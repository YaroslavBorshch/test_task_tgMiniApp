<template>

  <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company" />
      <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Choose your birthday</h2>
    </div>

    <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">

      <BirthdayForm @submit="handleSubmit"/>


    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useMainStore } from '../stores/mainStore.ts';
import BirthdayForm from "../components/BirthdayForm.vue";
import { useRouter } from 'vue-router';
import {retrieveLaunchParams} from "@telegram-apps/sdk";

export default defineComponent({
  name: 'DatePickerPage',
  components: {
    BirthdayForm,
  },
  setup() {
    const mainStore = useMainStore();
    const isLoading = ref(false);
    const router = useRouter();

    const handleSubmit = async (formData: BirthdayForm) => {
      isLoading.value = true;
      try {
        const tg_info = JSON.stringify(retrieveLaunchParams());
        await mainStore.login(formData, tg_info);
        if (mainStore.status == 200) {
          await router.push('/birthdayInfo');
        }
      } catch (error) {
        mainStore.message = 'error at sending' + error;
        mainStore.user_exist = false;
      } finally {
        isLoading.value = false;
      }
    };

    return {
      handleSubmit,
      isLoading,
      mainStore
    };
  },
});
</script>