document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  email_view = document.querySelector('#email-view');
  emails_view = document.querySelector('#emails-view');
  compose_view = document.querySelector('#compose-view');

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  emails_view.style.display = 'none';
  compose_view.style.display = 'block';

  email_view.innerHTML = '';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Send email
  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value,
          read: false,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Error alert
        if (result['error']) {
          alert(result['error']);
        }
        else {
          load_mailbox('sent');
        }
    });
    return false;
  }
  
}

function load_mailbox(mailbox) {

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach((email) => {
      
      // Create email divs
      var emails_div = document.createElement('div');
      emails_div.className = `card p-3 my-3 ${email.read}`;

      if (mailbox == 'sent') {
        var from_email = email.recipients[0]
      }
      else {
        from_email = email.sender
      }

      emails_div.innerHTML = `
        <div class="row no-gutters">
          <div class="col-2">${from_email}</div>
          <div class="col-3 truncate">${email.subject}</div>
          <div class="col-5 ml-3 truncate">${email.body}</div>
          <div class="col-2 ml-auto"><em>${email.timestamp}</em></div>
        </div>
      `
      emails_div.style.cursor = 'pointer';
      emails_div.addEventListener('click', () => load_email(email.id, mailbox));
      emails_view.append(emails_div);
    });
      
  });
      
  // Show the mailbox and hide other views
  emails_view.style.display = 'block';
  compose_view.style.display = 'none';
  email_view.style.dislay = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Hide email view
  email_view.innerHTML = '';

}

function load_email(id, mailbox) {

  email_view.innerHTML = '';
  
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Display email
      email_view.innerHTML = `
      <span style="font-weight: bold">From: </span>${email.sender}<br>
      <span style="font-weight: bold">To: </span>${email.recipients}<br>
      <span style="font-weight: bold">Subject: </span>${email.subject}<br>
      <span style="font-weight: bold">Sent: </span>${email.timestamp}<br>
      <div class="email-buttons">
        <a href="#" id="reply">Reply</a>&nbsp;
        <a href="#" id="archive">${email.archived ? "Unarchive" : "Archive"}</a>
      </div>
      <hr>
      ${email.body}
      `;
      mark_read(email.id);

      if (mailbox == 'sent') {
        document.querySelector('#archive').style.display = 'none';
      }

      document.querySelector('#archive').addEventListener('click', () => {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
        .then(() => load_mailbox('inbox'));
      });

      document.querySelector('#reply').addEventListener('click', () => {
        compose_email();
        if (email.subject.slice(0,3) != 'Re:') {
          email.subject = `Re: ${email.subject}`;
        } 

        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = email.subject;
        document.querySelector('#compose-body').value = '\n\n\n' + `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`
      })
});


// Show the mailbox and hide other views
emails_view.style.display = 'none';
compose_view.style.display = 'none';
email_view.style.display = 'block';

}

function mark_read(email) {
  fetch(`/emails/${email}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}
