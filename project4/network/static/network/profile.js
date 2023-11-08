document.addEventListener('DOMContentLoaded', function() {
    
    const userid=document.querySelector('#userid')
        fetch(`/profileapi/${userid.dataset.user}`)
            .then(response => response.json())
            .then(posts => {console.log(posts)
                posts.forEach(function(post){
                    if (post.likebyuser==='yes'){
                        document.querySelector(`#heart${post.id}`).style.color="red";
                    }
                })
            });
    
    

    document.querySelectorAll('.heart').forEach( function(i){
        
        i.onclick=function(){

            fetch(`/likes/${i.dataset.id}`)
            .then(response => response.json())
            .then(posts => {console.log(posts)

            posts.forEach(function(post)
            {
                const likes=post.likes
                if (post.likebyuser==='no'){
                    if (document.querySelector(`#heart${post.id}`).style.color==="red"){
                        document.querySelector(`#heart${post.id}`).style.color="black";
                        document.querySelector(`#likes${post.id}`).innerHTML=likes;
                    }else{
                        document.querySelector(`#heart${post.id}`).style.color="red";
                        document.querySelector(`#likes${post.id}`).innerHTML=likes+1;
                    }
                
                } else if (post.likebyuser==='yes'){
                    if (document.querySelector(`#heart${post.id}`).style.color==="red"){
                        document.querySelector(`#heart${post.id}`).style.color="black";
                        document.querySelector(`#likes${post.id}`).innerHTML=likes-1;
                    }else{
                        document.querySelector(`#heart${post.id}`).style.color="red";
                        document.querySelector(`#likes${post.id}`).innerHTML=likes;
                    }
                };
            })
            });
            }})})    

    

    

