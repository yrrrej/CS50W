document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //Sending Email
  document.querySelector('form').onsubmit= (function() {
    const recipients=document.querySelector('#compose-recipients').value;
    const subject=document.querySelector('#compose-subject').value;
    const body=document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    });

    load_mailbox('sent');
    return false;
  });
})


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#singleemail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#singleemail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show content in mailbox
  // inbox
  if (mailbox==='inbox'){
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
        emails.forEach(add_mail)
  });
  //Sent
  } else if (mailbox==='sent'){
    fetch('/emails/sent')
    .then(response => response.json())
    .then(emails => {
        emails.forEach(add_mailsent)
  });
  //Archive
  } else {
    fetch('/emails/archive')
    .then(response => response.json())
    .then(emails => {
        emails.forEach(add_mail)
  });
  }
}

function add_mailsent(mail) {
  //Sentbox view
  const maildiv=document.createElement('div');
  maildiv.id='maildiv'
  maildiv.className='container bg-light';
  maildiv.innerHTML=`<div class="row border border-dark"> <div class="col"><strong>${mail.sender}</strong></div> <div class="col">Subject: ${mail.subject}</div> <div class="col-6"><p class="text-right text-secondary">${mail.timestamp}<p></div></div>`;
  maildiv.addEventListener('click',function(){      
  fetch(`/emails/${mail.id}`)
  .then(response => response.json())
  .then(email => {
      document.querySelector('#emails-view').style.display = 'none'
      document.querySelector('#singleemail-view').style.display = 'block'
      document.querySelector('#singleemail-view').innerHTML=`<div class="row"> 
      <div class="row"><strong>From: </strong> ${email.sender}</div> 
      <div class="w-100"></div>
      <div class="row"><strong>To: </strong> ${email.recipients}</div> 
      <div class="w-100"></div>
      <div class="row"><strong>Subject: </strong> ${email.subject}</div> 
      <div class="w-100"></div>
      <div class="row"><strong>Timestamp: </strong> ${email.timestamp}</div> 
      <div class="w-100"><hr></div>
      <div class="row"><p class="text-left">${email.body}</p></div>
      <div class="w-100"></div>
      </div>`
      ;
  });
  })
  document.querySelector('#emails-view').append(maildiv);
}

//inbox and archive view
function add_mail(mail) {
  const maildiv=document.createElement('div');
  maildiv.id='maildiv'
  if (mail.read===false){
    if (mail.archived===false){
      //if unread an unarchived
      maildiv.className='container';
      maildiv.innerHTML=`<div class="row border border-dark"> <div class="col"><strong>${mail.sender}</strong></div> <div class="col">Subject: ${mail.subject}</div> <div class="col-6"><p class="text-right text-secondary">${mail.timestamp}<p></div></div>`;
      maildiv.addEventListener('click',function(){
      //if mail div is clicked, mark as read
      fetch(`/emails/${mail.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
      //if mail div is clicked, display mail content
      fetch(`/emails/${mail.id}`)
      .then(response => response.json())
      .then(email => {
          document.querySelector('#emails-view').style.display = 'none'
          document.querySelector('#singleemail-view').style.display = 'block'
          document.querySelector('#singleemail-view').innerHTML=`<div class="row"> 
          <div class="row"><strong>From: </strong> ${email.sender}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>To: </strong> ${email.recipients}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Subject: </strong> ${email.subject}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Timestamp: </strong> ${email.timestamp}</div> 
          <div class="w-100"></div>
          <div class="row">
          <div><button type="button" id="reply" class="btn btn-outline-primary">Reply</button></div>
          <div><button type="button" id="archive" class="btn btn-outline-primary ml-2">Archive</button></div>
          </div>
          <div class="w-100"><hr></div>
          <div class="row"><p class="text-left">${email.body}</p></div>
          <div class="w-100"></div>
          </div>`
          ;
          //if archive buttion is clicked, archive the email
          document.querySelector('#archive').addEventListener('click',function(){
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: true
              })
            });

            load_mailbox('inbox');
            window.location.reload();

          })
          //if reply buttion is clicked, show compose view
          document.querySelector('#reply').addEventListener('click',function(){
            // Show compose view and hide other views
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';
            document.querySelector('#singleemail-view').style.display = 'none';
            
            //Prefill reply contents
            document.querySelector('#compose-recipients').value = `${email.sender}`;
            //Check if email subject starts with 'Re:'
            if (email.subject.startsWith('Re:')){
              document.querySelector('#compose-subject').value = `${email.subject}`;
            } else{
              document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
            } 
            document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}" `;
          })
      });
      })
    } else {
      //unread and archived
      maildiv.className='container';
      maildiv.innerHTML=`<div class="row border border-dark"> <div class="col"><strong>${mail.sender}</strong></div> <div class="col">Subject: ${mail.subject}</div> <div class="col-6"><p class="text-right text-secondary">${mail.timestamp}<p></div></div>`;
      maildiv.addEventListener('click',function(){
      //if mail div is clicked, mark as read
      fetch(`/emails/${mail.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
      //if mail div is clicked, display mail content
      fetch(`/emails/${mail.id}`)
      .then(response => response.json())
      .then(email => {
          document.querySelector('#emails-view').style.display = 'none'
          document.querySelector('#singleemail-view').style.display = 'block'
          document.querySelector('#singleemail-view').innerHTML=`<div class="row"> 
          <div class="row"><strong>From: </strong> ${email.sender}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>To: </strong> ${email.recipients}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Subject: </strong> ${email.subject}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Timestamp: </strong> ${email.timestamp}</div> 
          <div class="w-100"></div>
          <div class="row">
          <div><button type="button" id="unarchive" class="btn btn-outline-primary">Unarchive</button></div>
          </div>
          <div class="w-100"><hr></div>
          <div class="row"><p class="text-left">${email.body}</p></div>
          <div class="w-100"></div>
          </div>`
          ;
          //if unarchive buttion is clicked, unarchive the email
          document.querySelector('#unarchive').addEventListener('click',function(){
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: false
              })
            });

            load_mailbox('inbox');
            window.location.reload();
          })
      });
      })
    }
  } else {
    if (mail.archived===false){
      //read and unarchived
      maildiv.className='container bg-light';
      maildiv.innerHTML=`<div class="row border border-dark"> <div class="col"><strong>${mail.sender}</strong></div> <div class="col">Subject: ${mail.subject}</div> <div class="col-6"><p class="text-right text-secondary">${mail.timestamp}<p></div></div>`;
      maildiv.addEventListener('click',function(){
      //if mail div is clicked, display mail content
      fetch(`/emails/${mail.id}`)
      .then(response => response.json())
      .then(email => {
          document.querySelector('#emails-view').style.display = 'none'
          document.querySelector('#singleemail-view').style.display = 'block'
          document.querySelector('#singleemail-view').innerHTML=`<div class="row"> 
          <div class="row"><strong>From: </strong> ${email.sender}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>To: </strong> ${email.recipients}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Subject: </strong> ${email.subject}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Timestamp: </strong> ${email.timestamp}</div> 
          <div class="w-100"></div>
          <div class="row">
          <div><button type="button" id="reply" class="btn btn-outline-primary">Reply</button></div>
          <div><button type="button" id="archive" class="btn btn-outline-primary ml-2">Archive</button></div>
          </div>
          <div class="w-100"><hr></div>
          <div class="row"><p class="text-left">${email.body}</p></div>
          <div class="w-100"></div>
          </div>`
          ;
          //if archive buttion is clicked, archive the email
          document.querySelector('#archive').addEventListener('click',function(){
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: true
              })
            });

            load_mailbox('inbox');
            window.location.reload();
          })
          //if reply buttion is clicked, show compose view
          document.querySelector('#reply').addEventListener('click',function(){
            // Show compose view and hide other views
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'block';
            document.querySelector('#singleemail-view').style.display = 'none';
            
            //Prefill reply contents
            document.querySelector('#compose-recipients').value = `${email.sender}`;
            //Check if email subject starts with 'Re:'
            if (email.subject.startsWith('Re:')){
              document.querySelector('#compose-subject').value = `${email.subject}`;
            } else{
              document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
            } 
            document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}" `;
          })
      });
      })
    } else {
      //read and archived
      maildiv.className='container bg-light';
      maildiv.innerHTML=`<div class="row border border-dark"> <div class="col"><strong>${mail.sender}</strong></div> <div class="col">Subject: ${mail.subject}</div> <div class="col-6"><p class="text-right text-secondary">${mail.timestamp}<p></div></div>`;
      maildiv.addEventListener('click',function(){
      //if mail div is clicked, display mail content
      fetch(`/emails/${mail.id}`)
      .then(response => response.json())
      .then(email => {
          document.querySelector('#emails-view').style.display = 'none'
          document.querySelector('#singleemail-view').style.display = 'block'
          document.querySelector('#singleemail-view').innerHTML=`<div class="row"> 
          <div class="row"><strong>From: </strong> ${email.sender}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>To: </strong> ${email.recipients}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Subject: </strong> ${email.subject}</div> 
          <div class="w-100"></div>
          <div class="row"><strong>Timestamp: </strong> ${email.timestamp}</div> 
          <div class="w-100"></div>
          <div class="row">
          <div><button type="button" id="unarchive" class="btn btn-outline-primary">Unarchive</button></div>
          </div>
          <div class="w-100"><hr></div>
          <div class="row"><p class="text-left">${email.body}</p></div>
          <div class="w-100"></div>
          </div>`
          ;
          //if unarchive buttion is clicked, unarchive the email
          document.querySelector('#unarchive').addEventListener('click',function(){
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: false
              })
            });

            load_mailbox('inbox');
            window.location.reload();
          })
      });
      })
    }
  }
  //after if else, append maildiv to emails-view
  document.querySelector('#emails-view').append(maildiv)
}