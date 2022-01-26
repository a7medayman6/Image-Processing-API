const stringifyQuery = (obj) =>
  Object.keys(obj).map(k => k + '=' + encodeURIComponent(obj[k])).join('&');

export const GET = async (endpoint, params = {}) => {
  try {
    const hasQuery = JSON.stringify(params) !== '{}';
    const url = `/api/${endpoint}${hasQuery ? `?${stringifyQuery(params)}` : ''}`;
    console.log('GET Request:', url);
    const res = await fetch(url);
    return await res.json();
  } catch (error) {
    console.error('GET Error', error);
  }
};

export const bytesToSize = (bytes) => {
  var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  if (bytes == 0) return '0 Bytes';
  var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
  return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
};
