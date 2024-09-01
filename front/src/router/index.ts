import { createRouter, createWebHistory } from 'vue-router';
// import LoginPage from '../pages/LoginPage.vue';
// import DashboardPage from '../pages/DashboardPage.vue';
import DatePickerPage from "../pages/DatePickerPage.vue";
import BirthdayInfoPage from "../pages/BirthdayInfoPage.vue";
import { retrieveLaunchParams } from '@telegram-apps/sdk';

// Создаем экземпляр маршрутизатора с историей веб-приложения
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: DatePickerPage,
      // TODO:: скорее удобней вначале проверять лаунчпарам и в зависимости от этого направлять роут
      // тг апп направляет всегда ток на главный индекс, единственный варик - передать стартап аргумент
      // что бы не редиректить внутри компонентов обработаем этот момент на уровне роута
      beforeEnter: (to, from, next) => {
        const params = retrieveLaunchParams(); // Получаем параметры запуска
        const sharedParams = JSON.stringify(params); // Преобразуем параметры в строку JSON

        // Проверяем, содержат ли параметры свойство 'startParam'
        if (params.hasOwnProperty('startParam')) {
          // Если да, перенаправляем на BirthdayInfoPage с передачей параметров
          next({ name: 'BirthdayInfoPage', query: { sharedParams: sharedParams } });
        } else {
          // Иначе, разрешаем переход на LoginPage
          next();
        }
      },
    },
    {
      path: '/birthdayInfo',
      name: 'BirthdayInfoPage',
      component: BirthdayInfoPage,
      props: true, // Передаем параметры запроса как пропсы компоненту
    },
    {
      path: '/loginAgain',
      name: 'DatePickerPage',
      component: DatePickerPage,
    },
  ],
});

export default router;
