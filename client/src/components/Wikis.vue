<template>
  <div>
    <section class="section">
      <div class="container">
        <h1 class="title">Wikis</h1>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h2 class="title">Accessible Wikis</h2>
        <ul>
          <li v-for="wiki of accessible_wikis">
            <a
              v-bind:href="wiki.url"
            >{{wiki.wikiname}}</a>
          </li>
        </ul>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <h2 class="title">My Wikis</h2>
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
                    <div v-if="!wiki.createWikiFromCsv">
                      <button
                        class="button is-link"
                        type="button"
                        v-on:click="enableCsvPopulate(wiki)"
                      >
                        Populate Wiki with CSV Data
                      </button>
                    </div>
                    <div v-if="wiki.createWikiFromCsv">
                      <div class="field">
                        <label
                          class="label"
                        >Populate Wiki with CSV Data</label>
                        <input
                          type="hidden"
                          name="wiki_id"
                          v-bind:value="wiki.id"
                        />
                      </div>
                      <Csv2WikiImport />
                      <div class="field">
                        <div class="control">
                          <input
                            class="button is-link"
                            type="submit"
                            value="Populate Wiki with CSV"
                          >
                        </div>
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
            <h2 class="title is-4">Create a New Wiki</h2>
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
                  Populate the New Wiki with CSV Data
                </label>
              </div>
              <!--
                Bulma does form spacing via sibling divs with a class of
                'field', so conditionally include each 'field' div, rather than
                wrapping them in a conditional wrapper (which breaks spacing).
              -->
              <div v-if="createWikiFromCsv">
                <Csv2WikiImport />
              </div>

              <div class="field">
                <div class="control">
                  <input
                    class="button is-link"
                    type="submit"
                    v-bind:value="createWikiFromCsv ? 'Create New Wiki from CSV Data' : 'Create New Wiki'"
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
import Vue from 'vue';
import Csv2WikiImport from "./Csv2WikiImport.vue";

export default {
  name: "Wikis",
  components: {
    Csv2WikiImport
  },
  data() {
    return {
      wikis: [],
      accessible_wikis: [],
      createWikiFromCsv: false
    };
  },
  methods: {
    enableCsvPopulate(wiki) {
      Vue.set(wiki, 'createWikiFromCsv', true)
    },
    getWikisData() {
      axios
        .get("/wikis/wikisdata")
        .then(res => {
          this.accessible_wikis = res.data.accessible_wikis;
          this.wikis = res.data.mywikis;
          this.wikis.forEach(wiki => Vue.set(wiki, 'createWikiFromCsv', false));
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
