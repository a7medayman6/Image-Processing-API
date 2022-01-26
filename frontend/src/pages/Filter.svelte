<script>
  import { onMount } from 'svelte';

  import { GET } from '../utils';

  let images = [];
  let selectedImageName = null;
  let selectedFilter = 'original';
  let value = 1;
  
  const getAllImages = async () => {
    try {
      const res = await GET('all');
      console.log('/api/all => Response ->', res);
      if (Array.isArray(res)) images = res;
    } catch (error) {
      console.error('/api/all => Error ->', error);
    }
  };

	onMount(() => { getAllImages(); });
</script>


<div class="content">
  <div class="field">
    <label class="label" for="filter-input-select-image">Image</label>
    <div class="control">
      <div class="select">
        <select id="filter-input-select-image" bind:value={selectedImageName}>
          <option value={null}>None</option>
          {#each images as i}
            <option value={i.file_name}>{i.file_name}</option>
          {/each}
        </select>
      </div>
      <button class="button" on:click={getAllImages}>Refresh Image List</button>
    </div>
  </div>
  <div class="field">
    <label class="label" for="filter-input-select-filter">Filter</label>
    <div class="control">
      <div class="select">
        <select id="filter-input-select-filter" bind:value={selectedFilter}>
          <option value="original">Original</option>
          <option value="grayscale">Grayscale</option>
          <option value="crop">Crop</option>
          <option value="downsample">Downsample</option>
          <option value="normalize">Normalize</option>
          <option value="power_spectrum">Power Spectrum</option>
        </select>
      </div>
    </div>
  </div>
  <div class="field">
    <label class="label" for="filter-input-value" >Value (Query Param)</label>
    <div class="control">
      <input id="filter-input-value" class="input" type=number bind:value={value}>
    </div>
  </div>
</div>

{#if selectedImageName}
  <p>{selectedImageName}</p>
  <img src="/api/filter/{selectedImageName.split('.')[0]}/{selectedFilter}?value={value}" alt={selectedImageName}/>
{:else}
  <p>Select an image</p>
{/if}
