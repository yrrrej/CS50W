document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('.divbutton').forEach(function(divbutton){
        divbutton.style.display='none'
        divbutton.addEventListener('click',()=>{
                
            if (document.querySelector(`#divform${divbutton.dataset.id}`).style.display==='block'){
                document.querySelector(`#divform${divbutton.dataset.id}`).style.display='none'
                document.querySelector(`#divcontent${divbutton.dataset.id}`).style.display='block'
                console.log(document.querySelector(`#contents${divbutton.dataset.id}`).value)
            } else{
                document.querySelector(`#divform${divbutton.dataset.id}`).style.display='block'
                document.querySelector(`#divcontent${divbutton.dataset.id}`).style.display='none'
            }
        })
    })


    document.querySelectorAll('.divform').forEach(function(divform){
        divform.style.display='none'
    })

    fetch(`/followingapi`)
        .then(response => response.json())
        .then(posts => {console.log(posts)
            posts.forEach(function(post){
                if (post.likebyuser==='yes'){
                    document.querySelector(`#heart${post.id}`).style.color="red";
                };

                if (post.ownpost===true){
                    document.querySelector(`#divbutton${post.id}`).style.display='block'
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

