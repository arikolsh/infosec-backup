<!DOCTYPE html>
<html>
  <head>
    <title>Slack-Off @ NSK - Login</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-2.2.3.min.js" integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo=" crossorigin="anonymous"></script>
    <script>
      $(document).ready(function() {
        $('#login').submit(function() {
          if (!$('#username').val()) {
            alert('Please insert a username.');
            return false;
          }
          if (!$('#password').val()) {
            alert('Please insert a password.');
            return false;
          }
        });
      });
    </script>
  </head>
  <body>
    <div class="container">
      <h1>Slack-off @ NSK <small>Because 90s chat-rooms are back in fashion</small></h1>
      <p>To use the chat, please log in below.</p>
      <form id="login" action="/login" method="post">
        <div class="form-group">
          <label for="username">Username: </label>
          <input type="input" class="form-control" id="username" name="username" />
        </div>
        <div class="form-group">
          <label for="password">Password: </label>
          <input type="password" class="form-control" id="password" name="password" />
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>
    </div>
  </body>
</html>
