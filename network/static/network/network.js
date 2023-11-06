
const token = getCookie('csrftoken');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function loadpage(pagetype){
	if(pagetype == "prev"){
		page = document.getElementById("pageprev").getAttribute("data-page");
	}	
	else{
		page = document.getElementById("pagenext").getAttribute("data-page");
	}
	load_posts(page);
	document.getElementById("pageprev").setAttribute("data-page", (parseInt(page) - 1).toString())
	document.getElementById("pagenext").setAttribute("data-page", (parseInt(page) + 1).toString())
}

function load_posts(page = 1) {

	let follow = false; 
	if(document.getElementById("following").getAttribute("data-following") == 'True'){
		document.getElementById("Head").innerHTML = "Following"
		follow = true;
	}
	else{
		document.getElementById("Head").innerHTML = "All Posts";	
	}
	x = document.querySelector('#posts-list');
	if(x){	
		if(follow){
			x.innerHTML = "";
			fetch('/loadfollowing/'+page.toString())
			.then(response => response.json())
			.then(posts => {
				posts.forEach(function(post) {disaply_post(post, false);});
				document.querySelector('#pageno').innerHTML = "Page " + page.toString() + " of " + posts[0].pagecount;
				if(page.toString() == posts[0].pagecount){
					document.querySelector("#pagenext").style.pointerEvents = "none";
				}
				else{
					document.querySelector("#pagenext").style.pointerEvents = "";
				}
				if(page == 1){
					document.querySelector("#pageprev").style.pointerEvents = "none";
				}
				else{
					document.querySelector("#pageprev").style.pointerEvents = "";
				}				
				});			
		}
		else{
			x.innerHTML = "";
			fetch('/posts/page/'+page.toString())
			.then(response => response.json())
			.then(posts => {
				posts.forEach(function(post) {disaply_post(post, false)});
				document.querySelector('#pageno').innerHTML = "Page " + page.toString() + " of " + posts[0].pagecount;
				if(page.toString() == posts[0].pagecount){
					document.querySelector("#pagenext").style.pointerEvents = "none";
				}	
				else{
					document.querySelector("#pagenext").style.pointerEvents = "";
				}							
				if(page == 1){
					document.querySelector("#pageprev").style.pointerEvents = "none";
				}
				else{
					document.querySelector("#pageprev").style.pointerEvents = "";
				}
				});
		}
	}		
}
function load_userposts(userid) {
	x = document.querySelector('#posts-list');
	//~ let isprofile = false;
	//~ if (document.getElementById("ProfileURL") == null)
		//~ isprofile=true;
	if(x){	
		x.innerHTML = "";
		fetch(`/${userid}`)			
		.then(response => response.json())
		.then(posts => {
			posts.forEach(function(post) {disaply_post(post, true)});
			});
		//~ document.getElementById("head").innerHTML = "User Posts";	
	}	
}
function disaply_post(post, isprofile){
	
	postdate = post.post_date; //new Date(post.date).toLocaleDateString('en-us', { weekday:"long", year:"numeric", month:"short", day:"numeric"});
	x = document.querySelector('#posts-list');	
	liketype = ""
	if(post.liked){
		liketype = 'Unlike';
		datalike = 0;
	}
	else{
		liketype = 'Like';
		datalike = 1;
	}	
	let likeml = "";		
	if((post.currentuser) != null){
		if(post.currentuser != post.user_id)
			likeml = `<a id='like' href=#post${post.id} data-like="${datalike}" data-postid="${post.id}" onclick="toggleLike(this);">${liketype}</a>`
		else 
			if(isprofile == false)
				likeml = `<a id='like' href=# data-postid="${post.id}" onclick="edit(this);">Edit</a>`
	}	
	let namelink = "";
	if (isprofile){
		namelink = post.username;
	}
	 else{
		namelink = `<a id="a${post.id}" href=#> ${post.username} </a>`;
	}
		

	x.innerHTML += `<div class="post">
				<hr/>
						<div class="grid-container">
							<div class="item1 sm">by ${namelink} on ${postdate}</div>
							<div class="item2 colright sm">${likeml}</div>
							<div id="divcontent${post.id}" class="item3"> ${post.content} </div>
							<div id="div${post.id}" class="item4 sm">likes: ${post.likes} </div>
						</div>
				
				</div>`;
	 
	 	//~ x.innerHTML += `<div class="post">
				//~ <hr/>
						//~ <div class="col-sm"> ${namelink} </div>
						//~ <div class="col-sm"> ${post.content} </div>
						//~ <div class="col-sm colright"> ${postdate} </div>
						//~ <div id="div${post.id}" class="col-sm colright"> ${post.likes} </div>
						//~ <div class="col-sm colright">${likeml}</div>
				
				//~ </div>`;

	if (isprofile == false){
		as = document.getElementById('a'+post.id);
		profileURL = document.getElementById("ProfileURL").getAttribute("data-url");
		as.href = profileURL; 			
		as.href = as.href.replace("-9999", post.user_id);	
	}	
}

function toggleLike(element){
	//~ return false;
	like = element.getAttribute('data-like');
	fetch('/like', {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			like: like,
			postid: element.getAttribute('data-postid')
		})
	})
	.then(response => response.json())
	.then (data => setLike(element, data.likes)); //alert(likes.likes);return false;})
	
}	
function toggleFollow(element){
	followadd = element.getAttribute('data-follow');
	followuser = element.getAttribute('data-userid');
	fetch('/follow', {
		method: 'PUT',
		body: JSON.stringify({
			follow: followuser,
			followadd: followadd
		})
	})
	.then (setFollow(element));
	return false;	
}
function setFollow(element){
	followadd = element.getAttribute('data-follow');
	countdiv = document.getElementById('divFollowed');
	count = parseInt(countdiv.innerHTML);
	if(followadd == 1){
		element.setAttribute('data-follow', 0);
		element.innerHTML = 'Unfollow';
		count += 1;		
	}
	else{
		element.setAttribute('data-follow', 1);
		element.innerHTML = 'Follow';		
		count -= 1;
	}	
	countdiv.innerHTML = count;	
	return false;
}
function setLike(element, likes){
	countdiv = document.getElementById('div'+element.getAttribute('data-postid'));
	countdiv.innerHTML = "likes " + likes;
	if(element.innerHTML == 'Like'){
		element.innerHTML = 'Unlike';
		element.setAttribute('data-like', 0)
	}	
	else{
		element.innerHTML = 'Like';
		element.setAttribute('data-like', 1);
	}
		
	//~ like = element.getAttribute('data-like');
	//~ countdiv = document.getElementById('div'+element.getAttribute('data-postid'))
	//~ count = parseInt(countdiv.innerHTML);
	//~ if(like == 1){
		//~ element.setAttribute('data-like', 0);
		//~ element.innerHTML = 'Unlike';
		//~ count += 1;
	//~ }
	//~ else{
		//~ element.setAttribute('data-like', 1);
		//~ element.innerHTML = 'Like';		
		//~ count -= 1;
	//~ }	
	//~ countdiv.innerHTML = count;

}
function edit(element){
	postid = element.getAttribute('data-postid');
	fetch(`/posts/${postid}`)
		.then(response => response.json())
		.then(post => {
			document.getElementById("txtPost").value = post.content;
			})
	btn = document.getElementById('btnNew');
	btn.onClick="editpost(this);";
	btn.value = "Save";
	document.getElementById("bntCancel").style.display = "inline-block";
	localStorage.setItem("PostID", postid);
	return false;		
}

function newpost(element){
	if(element.onClick == "editpost(this);"){
		editpost(element);
		return false;
	}
	fetch(`/new`, {
		method: 'POST',
		body: JSON.stringify({
			content: document.getElementById("txtPost").value
		}),
	headers: { "X-CSRFToken": token },	
	})
	.then (x => {document.getElementById("txtPost").value = "";load_posts();});
	return false;		
}
function editpost(element){
	fetch(`/new`, {
		method: 'PUT',
		body: JSON.stringify({
			content: document.getElementById("txtPost").value,
			postid: localStorage.getItem("PostID")
		}),
		headers: { "X-CSRFToken": token }		
	})
	.then(post => {
		element.onClick = "newpost(this);"
		postElement = document.getElementById("divcontent"+localStorage.getItem("PostID"))
		postElement.innerHTML = document.getElementById("txtPost").value;
		document.getElementById("txtPost").value = "";
		document.getElementById("btnNew").value ="Post";
		document.getElementById('bntCancel').style.display = "none"
		postElement.scrollIntoView();
		})
	return false;
}
function cancelEdit(){
	document.getElementById("txtPost").value = "";
	document.getElementById("btnNew").value = "Post";
	document.getElementById("bntCancel").style.display = "none";
	document.getElementById("btnNew").onClick="newpost(this);";
	
}
