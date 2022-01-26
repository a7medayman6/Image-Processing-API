<script>
  import { Link } from 'svero';

  import { currentPath } from '../store';

  export let href;
</script>

<Link {href} className={$currentPath === href ? 'is-active' : ''}>
  <slot></slot>
</Link>
