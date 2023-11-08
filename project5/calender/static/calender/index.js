document.addEventListener('DOMContentLoaded', function() {
    
    const month=document.querySelector('#up').dataset.month
    const year=document.querySelector('#up').dataset.year


    document.querySelector('#inputevent').style.display='none'

    document.querySelectorAll('.card-body').forEach(function(date){
        date.addEventListener('click',function(){

            let day=date.dataset.date
            let month=date.dataset.month

            document.querySelector('#addeventlabel').innerHTML=`Add event on ${day}/${month}`

            document.querySelector('#addevent').addEventListener('submit',()=>{
                fetch('', {
                    method: 'PUT',
                    body: JSON.stringify({
                        day: day,
                        month: month,
                        eventname: document.querySelector('#eventname').value,
                        description: document.querySelector('#description').value,
                        from: document.querySelector('#from').value,
                        till: document.querySelector('#till').value,
                        year: year
                    })
                  });

            })
            
            
            if (document.querySelector('#inputevent').style.display==='none'){
                document.querySelector('#inputevent').style.display='block'
            } else{
                document.querySelector('#inputevent').style.display='none'
            }
            
        })
    })


    fetch(`/events/${year}/${month}`)
        .then(response => response.json())
        .then(events => {console.log(events)
            events.forEach(function(event){
                document.querySelector(`#d${event.day}`).className='col-sm border border-light bg-warning';
            })
        });
    
})

