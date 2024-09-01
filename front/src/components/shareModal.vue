<template>
  <div as="template" @click.stop="closeOnOutsideClick">
    <div class="relative z-10" >
      <div as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </div>

      <div     class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div class="flex min-h-full items-start justify-center p-4 text-center sm:items-center sm:p-0">
          <div ref="changeLinkModal"  as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <div class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
              <div class="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                <div class="sm:flex sm:items-start">
                  <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">

                  </div>
                  <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <div as="h3" class="text-base font-semibold leading-6 text-gray-900">Share your day!</div>
                    <div class="mt-5">
                      <p class="text-sm text-gray-500">You also can custom your shared link!</p>
                      <br>

                    </div>
                  </div>
                </div>
              </div>

              <span class="absolute top-4 right-4 cursor-pointer hover:text-gray-500" @click="$emit('close')">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
              </span>

              <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <template v-if="!changeLinkStore.in_progress">
                  <a type="button" :href="sharedLink" class="inline-flex w-full justify-center rounded-md bg-blue-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-400 sm:ml-3 sm:w-auto" @click="$emit('close')">Share!</a>
                  <input type="text" v-model="inputText" @change="$emit('update', inputText)" class="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:mr-3" placeholder="Введите ссылку">
                </template>
                <template v-else>
                  <button disabled type="button" class="disabled inline-flex w-full justify-center rounded-md bg-grey-500 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-grey-400 sm:ml-3 sm:w-auto" @click="$emit('close')">Validating..</button>
                  <input type="text" disabled class="disabled flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:mr-3" placeholder="Введите ссылку">
                </template>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

const open = ref(true)


import { useChangeLinkStore } from "../stores/changeLinkStore.ts";

export default defineComponent({
  name: 'ShareModal',
  props: {
    tg_info: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const changeLinkStore = useChangeLinkStore();
    const showModal = ref(true);
    const inputText = ref(props.tg_info['self_link']);
    const sharedLink = ref("https://t.me/share/url?url=https://t.me/test_dateSpreaderBot/spreadDate?startapp="+props.tg_info['self_link'])

    // watch для отслеживания изменений inputText
    watch(inputText, (newValue) => {
      // Обновление ссылки sharedLink, если inputText изменился
      sharedLink.value = "https://t.me/share/url?url=https://t.me/test_dateSpreaderBot/spreadDate?startapp="+newValue;
    });

    return {
      showModal,
      inputText,
      sharedLink,
      changeLinkStore,
    };
  },
  methods: {
    closeOnOutsideClick(event) {

      // Проверяем, был ли клик сделан внутри элемента с ref "myElement"
      if (this.$refs.changeLinkModal === null
          || event.target === this.$refs.changeLinkModal
          || this.$refs.changeLinkModal.contains(event.target
        )) {
        console.log("инсайд");
      } else {
        console.log("аутсайд");
        this.$emit('close');
      }
    }
  }
});
</script>
