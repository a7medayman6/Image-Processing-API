<script>
  import Header from './Header.svelte';
  import Navigation from './Navigation.svelte';
</script>

<main>
  <section class="hero is-light">
    <div class="hero-body">
      <div class="container">
        <div class="columns">
          <div class="column is-2">
          </div>
          <div class="column is-10">
            <Header />
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-2">
          <Navigation />
        </div>
        <div class="column is-10">
          <slot></slot>
        </div>
      </div>
    </div>
  </section>
</main>
<footer class="footer">
  <div class="content has-text-centered">
    <p>Structura Biotechnology Software Engineer Tech Challenge</p>
  </div>
</footer>
