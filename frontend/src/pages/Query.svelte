<script>
  import { onMount } from 'svelte';

  import { GET } from '../utils';

  let images = [];

  let maxWidth = 5000;
  let minArea = 1;
  let maxSizeBytes = 1;
  
  const getImages = async () => {
    try {
      const res = await GET('query', { max_width: maxWidth, min_area: minArea, max_size_bytes: maxSizeBytes });
      console.log('/api/query => Response ->', res);
      if (Array.isArray(res)) images = res;
    } catch (error) {
      console.error('/api/query => Response ->', error);
    }
  };

	onMount(() => { getImages(); });
</script>


<div class="content">
  <div class="field">
    <label class="label" for="query-input-max-width">Max Width (Pixels): {maxWidth}</label>
    <div class="control">
      <input id="query-input-max-width" class="input is-small" type=number on:change={() => getImages()} bind:value={maxWidth} min=0 max=5000>
      <input type=range class="full-width" on:mouseup={() => getImages()} bind:value={maxWidth} min=0 max=5000>
    </div>
  </div>
  <div class="field">
    <label class="label" for="query-input-min-area">Min Area (Pixels): {minArea}</label>
    <div class="control">
      <input id="query-input-min-area" class="input is-small" type=number on:change={() => getImages()} bind:value={minArea} min=0 max=10000000>
      <input type=range class="full-width" on:mouseup={() => getImages()} bind:value={minArea} min=0 max=10000000>
    </div>
  </div>
  <div class="field">
    <label class="label" for="query-input-max-size-bytes">Maximum Size of Image in Bytes: {maxSizeBytes}</label>
    <div class="control">
      <input id="query-input-max-size-bytes" class="input is-small" type=number on:change={() => getImages()} bind:value={maxSizeBytes} min=0 max=10000000>
      <input type=range class="full-width" on:mouseup={() => getImages()} bind:value={maxSizeBytes} min=0 max=10000000>
    </div>
  </div>
  <div class="field">
    <span class="label">Matching Images: {images.length}</span>
  </div>
  <table>
    <thead>
      <tr>
        <td>#</td>
        <td>Preview</td>
        <td>File Name</td>
      </tr>
    </thead>
    <tbody>
      {#each images as i, index}
        <tr>
          <td>{index + 1}</td>
          <td>
            <img src="/api/filter/{i.split('.')[0]}/original" alt={i} style="max-width: 100px;"/>
          </td>
          <td>{i}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
