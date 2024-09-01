<template>

<div class="container flex flex-col items-center justify-center w-full mx-auto">
    <div class="w-full px-4 py-5 mb-2 bg-white border rounded-md shadow sm:px-6 dark:bg-gray-800">
        <h3 class="text-lg font-medium leading-6 text-gray-900 dark:text-white">
            Countdown to birthday!
        </h3>
        <p v-if="timeLeft && mainStore.status == 200" class="max-w-2xl mt-1 text-sm text-gray-500 dark:text-gray-200">
            {{ timeLeft.days }} дней, {{ timeLeft.hours }} часов, {{ timeLeft.minutes }} минут, {{ timeLeft.seconds }} секунд
        </p>
    </div>

    <template v-if="Object.keys(mainStore.tg_info).length != 0">

      <!-- Модальное окно -->
      <ShareModal
        v-if="showModal"
        :tg_info="mainStore.tg_info"
        @close="showModal = false"
        @update="handleShareLinkUpdate"
      />
    <ul class="flex flex-col">
        <li class="flex flex-row mb-2 border-gray-400" v-for="(value, key) in mainStore.tg_info">
            <div v-if="['self_link', 'is_serialized'].indexOf(key) == -1" class="shadow border select-none cursor-pointer bg-white dark:bg-gray-800 rounded-md flex flex-1 items-center p-4">
                <div class="flex-1 pl-1 md:mr-16">
                    <div class="font-medium dark:text-white">
                        {{ key }}
                    </div>
                    <div class="text-sm text-gray-600 dark:text-gray-200">

                    </div>
                </div>
                <div class="flex justify-end w-24 text-right">
                    <span width="12" fill="currentColor" height="12" class="text-gray-500 hover:text-gray-800 dark:hover:text-white dark:text-gray-200" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                    </span>
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-200">
                    {{ value }}
                </div>
                <div class="flex justify-end w-24 text-right">
                    <span width="12" fill="currentColor" height="12" class="text-gray-500 hover:text-gray-800 dark:hover:text-white dark:text-gray-200" viewBox="0 0 1792 1792" xmlns="http://www.w3.org/2000/svg">
                    </span>
                </div>
            </div>
        </li>
    </ul>

    </template>

    <template v-else>
      <div id="alert-additional-content-5" class="p-4 border border-gray-300 rounded-lg bg-gray-50 dark:border-gray-600 dark:bg-gray-800" role="alert">
        <div class="flex items-center">
          <svg class="flex-shrink-0 w-4 h-4 me-2 dark:text-gray-300" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
          </svg>
          <span class="sr-only">Info</span>
          <h3 class="text-lg font-medium text-gray-800 dark:text-gray-300">Кажется данных по этой ссылке не существует</h3>
        </div>
        <div class="mt-2 mb-4 text-sm text-gray-800 dark:text-gray-300">
        </div>
      </div>
    </template>
    <div class="w-full px-4 py-5 mb-2 bg-white border rounded-md shadow sm:px-6 dark:bg-gray-800 flex justify-between items-center">

      <a href="/loginAgain" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
        <!--  TODO:: сделать логику подгрузки сохраненной даты если уже зареган     -->
        <span v-if="mainStore.user_exist"> Change Birthday </span> <span v-else> Create account </span>
      </a>

      <button v-if="mainStore.user_exist && Object.keys(mainStore.tg_info).length != 0" @click="showModal = true" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
        Share
      </button>

    </div>

</div>

</template>

<script lang="ts">
import { retrieveLaunchParams } from '@telegram-apps/sdk';
import { defineComponent, ref, computed, onMounted, onUnmounted, watch} from 'vue';
import { useMainStore } from '../stores/mainStore.ts';
import { useChangeLinkStore } from "../stores/changeLinkStore.ts";
import ShareModal from "../components/shareModal.vue";
import { useRoute } from "vue-router";

export default defineComponent({
  name: 'BirthdayInfoPage',
  components: {
    ShareModal,
  },
  setup() {
    const mainStore = useMainStore();
    const changeLinkStore = useChangeLinkStore();
    const isLoaded = ref(false);
    const showModal = ref(false);
    const timeLeft = ref<{ days: number, hours: number, minutes: number, seconds: number } | null>(null);
    let intervalId: number;

    // посчитаем скок времени будем считать
    const calculateTimeLeft = () => {
      const now = new Date();
      let nextBirthday = new Date(mainStore.tg_info['birthday']);

      // Если день рождения уже прошел в этом году, добавляем год
      if (now > nextBirthday) {
        nextBirthday.setFullYear(nextBirthday.getFullYear() + 1);
      }
      // Получаем дельту
      const difference = nextBirthday.getTime() - now.getTime();
      // расчитываем отдельные части разницы для красивого отображения
      if (difference > 0) {
        const totalSeconds = Math.floor(difference / 1000);
        const days = Math.floor(totalSeconds / 86400);
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        timeLeft.value = { days, hours, minutes, seconds };
      } else {
        timeLeft.value = null;
      }
    };

    // отобразим модалку из стейка как ток получим его (либо из логина установлен будет либо из линка подтянем)
    const showEditModal = computed(() => {
      return mainStore.user_exist;
    });
    // отслеживаем ончейнж (точнее когда мы убрали активность с инпута изменения линка)
    const handleShareLinkUpdate = async (data: string) => {
      mainStore.tg_info['self_link'] = data;
      // отправляем запрос на проверку и обнову линка
      try {
          await  changeLinkStore.changeLink(data, mainStore.tg_info['tg_id']);
        } catch (error) {
          mainStore.message = 'error at sending' + error;
      }

    };

    // проверяем были ли переданы нам параметры
    const route = useRoute();

    const linkToShare = ref(route.query.sharedParams);
    try {
      // найдем регуляркой вхождение слово старт парам и возьмем все значения до первой ковычки
      // тк 100 проц известно, что первая ковычка - это некст ключ (главное что бы старт_парам в конце не стоял))
      const regex = /"startParam":"([^"]*)",/;
      const match = linkToShare.value.match(regex); // TODO <- may be null
      if (match) {
        // const shared_link = match[1];
        linkToShare.value = match[1];
      }
    } catch (error) {
      linkToShare.value = "";
    }


    onMounted(async () => {
      isLoaded.value = true;

      if (mainStore.from_login)
      {
          calculateTimeLeft();
          intervalId = setInterval(calculateTimeLeft, 1000);
      }
      // Если нет данных для отображения, то значит мы попали сюда по ссылке
      else if (!Object.keys(mainStore.tg_info).length)
      {
        // подгружаем инфу о текущем пользователе
        const tg_info = JSON.stringify(retrieveLaunchParams());
        try {
          await  mainStore.fetchUserData(linkToShare.value, tg_info);

          if (mainStore.status == 200)
          {
            calculateTimeLeft();
            intervalId = setInterval(calculateTimeLeft, 1000);
          }

        } catch (error) {
          mainStore.message = 'error at sending' + error;
          mainStore.user_exist = false;
        }
      }


    });

    onUnmounted(() => {
      clearInterval(intervalId);
    });


    return {
      isLoaded,
      mainStore,
      showEditModal,
      showModal,
      timeLeft,
      linkToShare,
      handleShareLinkUpdate,
    };
  },
});
</script>