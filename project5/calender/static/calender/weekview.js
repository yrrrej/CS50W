document.addEventListener('DOMContentLoaded', function() {




    fetch('/weekevent')
        .then(response => response.json())
        .then(events => {console.log(events)
            events.forEach(function(event){
                let i=Number(event.whenhour.slice(-4))
                let end=Number(event.tillhour.slice(-4))
                let date=event.whenhour.slice(0,-4)

                let randomColor = Math.floor(Math.random()*16777215).toString(16)
                document.querySelector(`#d${event.whenhour}`).style.backgroundColor='#'+randomColor;
                document.querySelector(`#d${event.tillhour}`).style.backgroundColor='#'+randomColor;
                document.querySelector(`#d${event.whenhour}`).innerHTML=`${event.eventname} start`;
                document.querySelector(`#d${event.tillhour}`).innerHTML=`${event.eventname} end`

                
                while (i<end) {
                    if (String(i).includes("3",2)){
                        i-=30
                        i+=100
                    } else if (String(i).includes("2",2)){
                        i-=30
                        i+=100
                    } else {
                        i+=30
                    }
                    document.querySelector(`#d${date}${i}`).style.backgroundColor='#'+ randomColor;
                }

                
            })
        });

})