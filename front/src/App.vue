<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import router from './router';

export default defineComponent({
  setup() {
    return {
      router,
    };
  },
});
</script>
<script setup lang="ts">
</script>