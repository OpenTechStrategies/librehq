<template>
  <div>
    <div class="field">
      <FileUploadInput
        inputLabel="Choose a CSV file…"
        inputName="csv"
      />
    </div>
    <div class="field">
      <div class="control">
        <label class="radio">
          <input
            type="radio"
            name="configuration"
            value="yesUseConfigForm"
            v-model="useConfigForm"
            checked
          />
          Enter config details
        </label>
        <br/>
        <label class="radio">
          <input
            type="radio"
            name="configuration"
            value=""
            v-model="useConfigForm"
          />
          Upload a config file
        </label>
      </div>
    </div>

    <div class="field" v-if="useConfigForm">
      <label class="label">Page Section Layout</label>
      <div class="field">
        Each row in the CSV file becomes a page in the wiki. The
        "Page Section Layout" specifies the common structure for the
        pages: what the page sections are, how they are nested, and
        which columns in the CSV go into which page sections.
        Each line has one of two forms:
     </div>
     <div class="field">
        1. If it begins with one or more dots ("."),
        it indicates the start of a new section.
        The number of dots indicates the nesting
        level: more dots means deeper subsection.
        After the dots comes an optional section
        title.  If you put "{N}" (N is an integer)
        in that title, it will be replaced with the
        column heading for column N.  Note this
        uses 1-based indexing: the first column is
        column 1, and there is no column 0.
      </div>
      <div class="field">
        2. If it starts with a number, then the
        current row's content for that column
        number is inserted into the page here.
        Everything after the number is ignored.
        Typically, one puts a comment there
        describing the column that corresponds to
        that number.
      </div>
      <div class="control">
        <textarea
          class="textarea"
          placeholder="Page Section Layout"
          name="pageSectionLayout"
          rows="10"
        ></textarea>
      </div>
    </div>

    <div class="field" v-if="useConfigForm">
      <label class="label">Page Title Template</label>
      <div class="field">
        The template into which selected column values from
        a row are substituted in order to create the title of
        the page generated from that row. Columns are specified
        with "{N}" in the string, where N is a column number.
        The special column "{0}" is the CSV row number
        (which is automatically left-padded with zeros
        appropriately for the total number of rows).
      </div>
      <div class="control">
        <input
          class="input"
          type="text"
          placeholder="Page Title Template"
          name="pageTitleTemplate"
        />
      </div>
    </div>

    <div class="field" v-if="useConfigForm">
      <label class="label">Title for the 'Table of Contents' Page</label>
      <div class="control">
        <input
          class="input"
          type="text"
          placeholder="TOC"
          value="TOC"
          name="toc"
        >
      </div>
    </div>

    <div class="field" v-if="useConfigForm">
      <label class="label">Category Column</label>
      <div class="field">
        The number of the column (if any) in the CSV
        file that should be used to create a category
        for that row. Column numbering begins at 1, not
        0. Leave blank to not use categories.
      </div>
      <div class="control">
        <input
          class="input"
          type="number"
          name="categoryColumn"
        />
      </div>
    </div>

    <div class="field" v-if="!useConfigForm">
      <FileUploadInput
        inputLabel="Choose a Config file…"
        inputName="config"
      />
    </div>
  </div>
</template>

<script>
import FileUploadInput from "./FileUploadInput.vue";

export default {
  name: "Csv2WikiImport",
  components: {
    FileUploadInput
  },
  data() {
    return {
      useConfigForm: "yesUseConfigForm"
    };
  }
};
</script>
