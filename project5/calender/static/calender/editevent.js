document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit').forEach(function(edit){
        edit.style.display='none'
    })

    document.querySelector('#whichevent').addEventListener('change',function(){
        document.querySelectorAll('.edit').forEach(function(edit){
            edit.style.display='none'
        })
        document.querySelector(`#editevent${this.value}`).style.display='block'
    })


})
