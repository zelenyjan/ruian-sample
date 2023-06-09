<script setup>
  defineProps({
    value: {
      required: true,
      type: [String, Number],
    },
    labelId: {
      type: String,
      default: "",
    },
  });
</script>

<template>
  <input :id="labelId" class="form-control" readonly :value="value" />
</template>
