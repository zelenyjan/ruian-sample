<script setup>
  defineProps({
    labelId: {
      type: String,
      default: "",
    },
    label: {
      required: true,
      type: String,
    },
  });
</script>

<template>
  <label :for="labelId" class="form-label">{{ label }}</label>
</template>
