<template>
  <div
    class="file"
    v-bind:class=" fileName ? 'has-name' : '' "
  >
    <label class="file-label">
      <input
        class="file-input"
        type="file"
        v-bind:name="inputName"
        @change="fileInputChange"
      >
      <span class="file-cta">
        <span class="file-icon">
          <font-awesome-icon icon="upload"></font-awesome-icon>
        </span>
        <span class="file-label">
          {{inputLabel}}
        </span>
      </span>
      <span
        v-if="fileName"
        class="file-name"
      >{{fileName}}</span>
    </label>
  </div>
</template>

<script>
export default {
  name: "FileUploadInput",
  props: {
    inputLabel: String,
    inputName: String
  },
  data() {
    return {
      fileName: false
    };
  },
  methods: {
    fileInputChange(event) {
      const input = event.target;
      if (input.files.length > 0) {
        this.fileName = input.files[0].name;
      }
    }
  }
};
</script>
