import json
from django.db import connection
from .models import *

def dictfetchall(cursor):

    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
    


def returnPosts (userid = -1, byuserid = None, following=False):
	cursor = connection.cursor()
	if not following:
		if not byuserid:
			if userid is not None:
				q= f"""select p.id, p.content, strftime('%Y-%m-%d %H:%M:%S',p.post_date) post_date, p.user_id, u.username, count(l.post_id) likes, l2.post_id liked
						from network_post p inner join network_user u on p.user_id = u.id
						left join network_likes l on l.post_id = p.id
						left join network_likes l2 on l2.post_id = p.id and l2.user_id = {userid}
						group by p.id,p.content,p.post_date,p.user_id,u.username
						order by p.id desc"""
			else:
				q= f"""select p.id, p.content, strftime('%Y-%m-%d %H:%M:%S',p.post_date) post_date, p.user_id, u.username, count(l.post_id) likes
						from network_post p inner join network_user u on p.user_id = u.id
						left join network_likes l on l.post_id = p.id
						group by p.id,p.content,p.post_date,p.user_id,u.username
						order by p.id desc"""
							
		else:
			q= f"""select p.id, p.content, strftime('%Y-%m-%d %H:%M:%S',p.post_date) post_date, p.user_id, u.username, count(l.post_id) likes, l2.post_id liked
					from network_post p inner join network_user u on p.user_id = u.id
					left join network_likes l on l.post_id = p.id
					left join network_likes l2 on l2.post_id = p.id and l2.user_id = {userid}
					where p.user_id = {byuserid}
					group by p.id,p.content,p.post_date,p.user_id,u.username
					order by p.id desc"""
	else:
		q= f"""select p.id, p.content, strftime('%Y-%m-%d %H:%M:%S',p.post_date) post_date, p.user_id, u.username, count(l.post_id) likes
						from network_post p inner join network_user u on p.user_id = u.id
						left join network_likes l on l.post_id = p.id
                        inner join network_follow f on f.user_id = {userid} and f.following_id = p.user_id 
						group by p.id,p.content,p.post_date,p.user_id,u.username
						order by p.id desc"""
	# ~ print(q)
	cursor.execute(q)
	result = dictfetchall(cursor)
	cursor.close()		
	# ~ print(result);
	return result

def toggleLike (userid,postid, like=True):
	cursor = connection.cursor()
	if like != "0":
		q=f"""insert into network_likes(post_id, user_id) 
			values ({postid},{userid})"""
	else:
		# ~ print('DELETE')
		q=f"delete from network_likes where post_id = {postid} and user_id = {userid}"
		# ~ print(q)
	result = cursor.execute(q)
# return post like count
	q=f"select count(post_id) likes from network_likes where post_id = {postid}"	
	cursor.execute(q)
	result = dictfetchall(cursor)
	cursor.close()	
#	sreturn = '{"result":"success"}'
	return {
			"likes": result[0]['likes']
		}	

def toggleFollow (userid, followuser, follow):
	cursor = connection.cursor()
	if follow != "0":
		q=f"""insert into network_follow(following_id, user_id) 
			values ({followuser},{userid})"""
	else:
		# ~ print('DELETE')
		q=f"delete from network_follow where following_id = {followuser} and user_id = {userid}"
		# ~ print(q)
	result = cursor.execute(q)
	cursor.close()	
	return result

def returnPost(postid):
	cursor = connection.cursor()
	q=f"SELECT CAST(id as text) id, content FROM network_post where id = {postid}"
	cursor.execute(q)
	result = dictfetchall(cursor)
	cursor.close()	
	post1 = result[0]
	return {
		"id": post1['id'],
		"content": post1['content']
	}	
def returnFollow(userid):
	# ~ using derived tables in query for one db call rather than 2
	cursor = connection.cursor()
	q=f"""select username, (select count(following_id) 
				from network_follow where user_id = {userid}) following,
				(select count(user_id) 
				from network_follow where following_id = {userid}) followed
			from network_user
			where id = {userid};"""
	cursor.execute(q)
	result = dictfetchall(cursor)
	cursor.close()	
	follows = result[0]		
	print(follows['username'])
	return {
		"username": follows['username'],
		"following": follows['following'],
		"followed": follows['followed']
	}
	
def returnIsFollowing(userid, followid):
	cursor = connection.cursor()
	q=f"""select count(id) isfollowing from network_follow where user_id = {userid} and following_id = {followid}"""
	cursor.execute(q)
	result = dictfetchall(cursor)
	cursor.close()
	if(int(result[0]["isfollowing"]) > 0):
		return True
	else:
		return False
