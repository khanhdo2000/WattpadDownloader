<script>
  import { onMount } from 'svelte';
  
  let storyId = '';
  let error = '';
  
  function handleSubmit(event) {
    event.preventDefault();
    
    if (!storyId.trim()) {
      error = 'Please enter a story ID';
      return;
    }
    
    if (!/^\d+$/.test(storyId.trim())) {
      error = 'Story ID must contain only numbers';
      return;
    }
    
    // Redirect to download link with MOBI format
    const downloadUrl = `/download/${storyId.trim()}?format=mobi&mode=story`;
    window.location.href = downloadUrl;
  }
</script>

<svelte:head>
  <title>Wattpad Downloader - Kindle</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</svelte:head>

<div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
  <div class="bg-white rounded-lg shadow-md p-8 w-full max-w-md">
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">WP Downloader</h1>
      <p class="text-gray-600">Download stories for your Kindle</p>
    </div>
    
    <form on:submit={handleSubmit} class="space-y-6">
      <div>
        <label for="storyId" class="block text-sm font-medium text-gray-700 mb-2">
          Story ID
        </label>
        <input
          type="text"
          id="storyId"
          bind:value={storyId}
          placeholder="Enter story ID (e.g., 237369078)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
        />
        {#if error}
          <p class="text-red-500 text-sm mt-1">{error}</p>
        {/if}
      </div>
      
      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200"
      >
        Download MOBI
      </button>
    </form>
    
    <div class="mt-6 text-center">
      <p class="text-sm text-gray-500">
        <a href="/" class="text-blue-600 hover:text-blue-800">← Back to main page</a>
      </p>
    </div>
    
    <div class="mt-8 text-xs text-gray-400 text-center">
      <p>How to get Story ID:</p>
      <p>1. Go to wattpad.com</p>
      <p>2. Find your story URL</p>
      <p>3. Copy the numbers from the URL</p>
      <p>Example: wattpad.com/story/237369078-title</p>
    </div>
  </div>
</div>

<style>
  /* Simple CSS for better Kindle compatibility */
  * {
    box-sizing: border-box;
  }
  
  body {
    margin: 0;
    font-family: Arial, sans-serif;
    line-height: 1.6;
  }
  
  .min-h-screen {
    min-height: 100vh;
  }
  
  .flex {
    display: flex;
  }
  
  .items-center {
    align-items: center;
  }
  
  .justify-center {
    justify-content: center;
  }
  
  .text-center {
    text-align: center;
  }
  
  .bg-gray-100 {
    background-color: #f3f4f6;
  }
  
  .bg-white {
    background-color: white;
  }
  
  .rounded-lg {
    border-radius: 0.5rem;
  }
  
  .shadow-md {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  
  .p-4 {
    padding: 1rem;
  }
  
  .p-8 {
    padding: 2rem;
  }
  
  .w-full {
    width: 100%;
  }
  
  .max-w-md {
    max-width: 28rem;
  }
  
  .mb-2 {
    margin-bottom: 0.5rem;
  }
  
  .mb-8 {
    margin-bottom: 2rem;
  }
  
  .mt-1 {
    margin-top: 0.25rem;
  }
  
  .mt-6 {
    margin-top: 1.5rem;
  }
  
  .mt-8 {
    margin-top: 2rem;
  }
  
  .text-3xl {
    font-size: 1.875rem;
  }
  
  .text-sm {
    font-size: 0.875rem;
  }
  
  .text-xs {
    font-size: 0.75rem;
  }
  
  .font-bold {
    font-weight: 700;
  }
  
  .font-medium {
    font-weight: 500;
  }
  
  .text-gray-800 {
    color: #1f2937;
  }
  
  .text-gray-600 {
    color: #4b5563;
  }
  
  .text-gray-700 {
    color: #374151;
  }
  
  .text-gray-500 {
    color: #6b7280;
  }
  
  .text-gray-400 {
    color: #9ca3af;
  }
  
  .text-red-500 {
    color: #ef4444;
  }
  
  .text-blue-600 {
    color: #2563eb;
  }
  
  .text-blue-800 {
    color: #1e40af;
  }
  
  .text-white {
    color: white;
  }
  
  .bg-blue-600 {
    background-color: #2563eb;
  }
  
  .bg-blue-700 {
    background-color: #1d4ed8;
  }
  
  .border {
    border-width: 1px;
  }
  
  .border-gray-300 {
    border-color: #d1d5db;
  }
  
  .rounded-md {
    border-radius: 0.375rem;
  }
  
  .px-3 {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }
  
  .py-2 {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .focus\:outline-none:focus {
    outline: none;
  }
  
  .focus\:ring-2:focus {
    box-shadow: 0 0 0 2px;
  }
  
  .focus\:ring-blue-500:focus {
    box-shadow: 0 0 0 2px #3b82f6;
  }
  
  .focus\:border-transparent:focus {
    border-color: transparent;
  }
  
  .hover\:bg-blue-700:hover {
    background-color: #1d4ed8;
  }
  
  .hover\:text-blue-800:hover {
    color: #1e40af;
  }
  
  .space-y-6 > * + * {
    margin-top: 1.5rem;
  }
  
  .block {
    display: block;
  }
  
  .transition {
    transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }
  
  .duration-200 {
    transition-duration: 200ms;
  }
</style>
