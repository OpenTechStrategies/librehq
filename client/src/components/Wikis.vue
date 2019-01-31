<template>
  <div>
    <section class="section">
      <div class="container">
        <h1 class="title">Wikis</h1>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="columns">
          <div
            class="column is-4"
            v-for="wiki of wikis"
            v-bind:key="wiki.id"
          >
            <div class="tile is-ancestor">
              <div class="tile is-vertical is-parent">

                <div class="tile is-child">
                  <h2 class="title is-4">{{wiki.wikiname}}</h2>
                  <a
                    v-bind:href="wiki.url"
                  >Visit {{wiki.wikiname}}</a>
                </div>

                <div class="tile is-child">
                  <form method="post" action="renamewiki">
                    <input
                      type="hidden"
                      name="wiki_id"
                      v-bind:value="wiki.id"
                    >
                    <div class="field">
                      <label class="label">Rename Wiki</label>
                      <div class="control">
                        <input
                          class="input"
                          type="text"
                          name="new_wiki_name"
                          placeholder="New Name"
                        >
                      </div>
                    </div>
                    <div class="field">
                      <div class="control">
                        <input
                          class="button is-link"
                          type="submit"
                          value="Rename Wiki"
                        >
                      </div>
                    </div>
                  </form>
                </div>

                <div class="tile is-child">
                  <form
                    action="uploadcsv"
                    method="post"
                    enctype="multipart/form-data"
                  >
                    <div class="field">
                      <label
                        class="label"
                      >Populate Wiki with CSV Data</label>
                      <input
                        type="hidden"
                        name="wiki_id"
                        v-bind:value="wiki.id"
                      />
                      <FileUploadInput
                        inputLabel="Choose a CSV file…"
                        inputName="csv"
                      />
                    </div>
                    <div class="field">
                      <FileUploadInput
                        inputLabel="Choose a Config file…"
                        inputName="config"
                      />
                    </div>
                    <div class="field">
                      <div class="control">
                        <input
                          class="button is-link"
                          type="submit"
                          value="Populate Wiki with CSV"
                        >
                      </div>
                    </div>
                  </form>
                </div>

                <div class="tile is-child">
                  <form method="post" action="deletewiki">
                    <input
                      type="hidden"
                      name="wiki_id"
                      v-bind:value="wiki.id"
                    >
                    <div class="field">
                      <label class="label">Delete Wiki</label>
                      <div class="control">
                        <!-- TODO: replace with non inline onclick code -->
                        <input
                          class="button is-danger"
                          type="submit"
                          value="Delete Wiki"
                          onclick='return confirm("Confirm Wiki Deletion");'
                        >
                      </div>
                    </div>
                  </form>
                </div>

              </div>
            </div>
          </div>

          <div class="column is-4">
            <h2 class="title is-4">Create a Wiki</h2>
            <form
              v-bind:action="createWikiFromCsv ? 'uploadcsv' : 'createwiki'"
              method="post"
              v-bind:enctype="createWikiFromCsv && 'multipart/form-data'"
            >
              <div class="field">
                <label class="label">Wiki Name</label>
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    name="name"
                    placeholder="Wiki Name"
                  >
                </div>
              </div>
              <div class="field">
                <label class="checkbox">
                  <input
                    type="checkbox"
                    v-model="createWikiFromCsv"
                  />
                  Populate the Wiki with CSV Data
                </label>
              </div>
              <!--
                Bulma does form spacing via sibling divs with a class of
                'field', so conditionally include each 'field' div, rather than
                wrapping them in a conditional wrapper (which breaks spacing).
              -->
              <div class="field" v-if="createWikiFromCsv">
                <FileUploadInput
                  inputLabel="Choose a CSV file…"
                  inputName="csv"
                />
              </div>
              <div class="field" v-if="createWikiFromCsv">
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

              <div class="field" v-if="createWikiFromCsv && useConfigForm">
                <label class="label">Page Section Layout</label>
                <div class="field">
                  Each wiki page corresponds to a row in the CSV. The
                  "Page Section Layout" shows the common structure for the
                  pages: what the section nesting is, and which
                  columns go in which sections in what order.
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

              <div class="field" v-if="createWikiFromCsv && useConfigForm">
                <label class="label">Page Title Template</label>
                <div class="field">
                  The template into which selected column values from
                  a row are substituted in order to create the title of
                  the page generated from that row. Columns are specified
                  with "{N}" in the string, where N is a column number.
                  The special column {0} is the CSV row number,
                  which is automatically left-padded with zeros
                  appropriately for the total number of rows.
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

              <div class="field" v-if="createWikiFromCsv && useConfigForm">
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

              <div class="field" v-if="createWikiFromCsv && useConfigForm">
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

              <div class="field" v-if="createWikiFromCsv && !useConfigForm">
                <FileUploadInput
                  inputLabel="Choose a Config file…"
                  inputName="config"
                />
              </div>

              <div class="field">
                <div class="control">
                  <input
                    class="button is-link"
                    type="submit"
                    v-bind:value="createWikiFromCsv ? 'Create Wiki from CSV Data' : 'Create Wiki'"
                  >
                </div>
              </div>

            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import FileUploadInput from "./FileUploadInput.vue";

export default {
  name: "Wikis",
  components: {
    FileUploadInput
  },
  data() {
    return {
      wikis: [],
      createWikiFromCsv: false,
      // gets set to empty string to match radio value & provide boolean behavior
      useConfigForm: "yesUseConfigForm"
    };
  },
  methods: {
    getWikisData() {
      axios
        .get("/wikis/wikisdata")
        .then(res => {
          this.wikis = res.data;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getWikisData();
  }
};
</script>
