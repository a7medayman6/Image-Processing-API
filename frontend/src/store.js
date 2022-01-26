import { writable, derived } from 'svelte/store';

export const currentPath = writable('');

export const pageTitle = derived(currentPath, $path => {
  if ($path === '/') return 'Introduction';
  else if ($path === '/all') return 'All Images';
  else if ($path === '/query') return 'Query Images';
  else if ($path === '/filter') return 'Filter Images';
  return '';
});
