<html><head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
  <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="/static/code.js"></script>
  <title>Slack-Off @ NSK</title>
  <script type="text/javascript">var username = "{{username}}";</script>
</head>

<body>
  <div class="container">
  <h1>Slack-off @ NSK</h1>
  <p>Welcome, {{name}} ({{username}}@)! Not you? <a href="/logout">Click here</a> to log out.</p>
  <p class="bg-warning" id="waiting">The page is still loading, please wait...</p>
  <div class="row">
    <div class="col-md-2">
      <h3>
        Channels
      </h3>
      <ul id="channel-area">
      </ul>
    </div>
    <div class="col-md-10">
      <h3>
        Current channel: <mark class="text-primary" id="current-channel"></mark>
      </h3>
      <table class="table table-striped">
        <thead>
          <tr><th>Date</th>
          <th>User</th>
          <th>Message</th>
        </tr></thead>
        <tbody id="message-area"></tbody>
      </table>
    </div>
  </div>

  <div class="row">
  <form class=".form-online" id="post" action="/post" method="post">
    <div class="form-group">
      <textarea class="form-control" id="message" name="message" placeholder="Your message here!"></textarea>
      <button type="submit" class="btn btn-default" id="submit">
        Submit
      </button>
    </div>
  </form>
  </div>
</div>
</body>
</html>
