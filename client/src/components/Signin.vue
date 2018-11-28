<template>
  <section class="section">
    <div class="container">
      <div class="columns">

        <div class="column">
          <h1 class="title">
            LibreHQ <em>beta</em>
          </h1>
          <p class="subtitle">
            This is the subtitle.
          </p>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </p>
        </div>

        <div class="column">
          <div class="title is-4">Sign up</div>
          <form action="signup" method="post">

            <div class="field">
              <label class="label">Username</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="text" name="username" placeholder="Username">
                <span class="icon is-small is-left">
                  <i class="fas fa-user"></i>
                </span>
              </div>
            </div>

            <div class="field">
              <label class="label">Password</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="password" name="password" placeholder="Password">
                <span class="icon is-small is-left">
                  <i class="fas fa-key"></i>
                </span>
              </div>
            </div>

            <div class="field">
              <label class="label">Email</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="email" name="email" placeholder="Email Address">
                <span class="icon is-small is-left">
                  <i class="fas fa-envelope"></i>
                </span>
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input class="button is-link" type="submit" value="Sign Up">
              </div>
            </div>

          </form>
        </div>

        <div class="column">
          <div class="title is-4">Sign in</div>
          <form action="signin" method="post">

            <div class="field">
              <label class="label">Username</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="text" name="username" placeholder="Username">
                <span class="icon is-small is-left">
                  <i class="fas fa-user"></i>
                </span>
              </div>
            </div>

            <div class="field">
              <label class="label">Password</label>
              <div class="control has-icons-left has-icons-right">
                <input class="input" type="password" name="password" placeholder="Password">
                <span class="icon is-small is-left">
                  <i class="fas fa-key"></i>
                </span>
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input class="button is-link" type="submit" value="Sign In">
              </div>
            </div>
          </form>
        </div>

      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "Signin"
};
</script>
