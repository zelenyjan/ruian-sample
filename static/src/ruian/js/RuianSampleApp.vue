<script setup>
  import { useScriptTag } from "@vueuse/core";
  import { ref } from "vue";
  import InputLabel from "src/components/InputLabel.vue";
  import ReadOnlyInput from "src/components/ReadOnlyInput.vue";
  import axios from "axios";
  import { axiosConfig } from "src/utils";

  useScriptTag("https://client.smartform.cz/v2/smartform.js", () => {
    // initialize smartform
    smartform.beforeInit = function () {
      smartform.setClientId("v1m4zrLM9Y");
    };
    smartform.afterInit = function () {
      const instance = smartform.getInstance();
      instance.addressControl.addValidationCallback(validationCallback);
    };
  });

  const addressData = ref(null);
  const cuzkData = ref(null);
  const addressInput = ref();

  const validationCallback = (result) => {
    if (result.result.type === smartform.AddressValidationResultType.HIT) {
      // on exact hit
      console.log(result.result.addressArray[0]);
      addressData.value = result.result.addressArray[0];
      const apiUrl = `/api/data/city/${addressData.value.CITY_CODE}/get_or_create_city/`;
      axios(apiUrl).then((response) => {
        cuzkData.value = response.data;
      });
    }
  };

  const submitAddressData = () => {
    const url = "/api/data/place/";
    const data = {
      address_data: addressData.value,
    };

    axios.post(url, data, axiosConfig).then((response) => {
      if (response.data.success) {
        alert("Uloženo");
        addressData.value = null;
        cuzkData.value = null;
        addressInput.value.value = "";
      }
      console.log(response.data);
    });
  };
</script>

<template>
  <div class="row mt-3">
    <div class="col-12">
      <form>
        <div>
          <label for="adresa" class="form-label">Adresa</label>
          <input
            id="adresa"
            ref="addressInput"
            type="text"
            class="form-control smartform-address-whole-address"
          />
        </div>
      </form>
    </div>
  </div>

  <template v-if="addressData">
    <div class="row mb-3">
      <h2>Data z smartform</h2>
      <h3>{{ addressData.FORMATTED_ADDRESS_WHOLE }}</h3>
      <div class="col-12">
        <InputLabel label="RUIAN" />
        <ReadOnlyInput :value="addressData.CODE" />
      </div>
    </div>
    <div class="row g-3">
      <div class="col-md-6">
        <InputLabel label="Popisné číslo" />
        <ReadOnlyInput :value="addressData.CONSCRIPTION_NUMBER" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Orientační číslo" />
        <ReadOnlyInput :value="addressData.STREET_NUMBER" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Evidenční číslo" />
        <ReadOnlyInput :value="addressData.PROVISIONAL_NUMBER" />
      </div>
      <div class="col-md-6">
        <InputLabel label="PSČ" />
        <ReadOnlyInput :value="addressData.ZIP" />
      </div>
    </div>
    <div class="row g-3 mt-1">
      <div class="col-md-6">
        <InputLabel label="Kód kraje" />
        <ReadOnlyInput :value="addressData.REGION_CODE" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Kraj" />
        <ReadOnlyInput :value="addressData.REGION" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Kód okresu" />
        <ReadOnlyInput :value="addressData.DISTRICT_CODE" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Okres" />
        <ReadOnlyInput :value="addressData.DISTRICT" />
      </div>

      <div class="col-md-6">
        <InputLabel label="Kód části obce" />
        <ReadOnlyInput :value="addressData.PART_CODE" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Část obce" />
        <ReadOnlyInput :value="addressData.PART" />
      </div>

      <div class="col-md-6">
        <InputLabel label="Kód ulice" />
        <ReadOnlyInput :value="addressData.STREET_CODE" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Ulice" />
        <ReadOnlyInput :value="addressData.STREET" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Kód města" />
        <ReadOnlyInput :value="addressData.CITY_CODE" />
      </div>
      <div class="col-md-6">
        <InputLabel label="Město" />
        <ReadOnlyInput :value="addressData.CITY" />
      </div>
    </div>
    <div class="row g-3 mt-1">
      <div class="col-12">
        <InputLabel label="dělení obcí – kód" />
        <ReadOnlyInput :value="addressData.CITY_AREA_1_CODE" />
      </div>
      <div class="col-12">
        <InputLabel label="dělení obcí – v ČR odpovídá městským částím" />
        <ReadOnlyInput :value="addressData.CITY_AREA_1" />
      </div>

      <div class="col-12">
        <InputLabel label="dělení obcí – kód" />
        <ReadOnlyInput :value="addressData.CITY_AREA_2_CODE" />
      </div>
      <div class="col-12">
        <InputLabel
          label="dělení obcí – v ČR odpovídá městským obvodům – v Praze je to 'Praha 1' - 'Praha 10'"
        />
        <ReadOnlyInput :value="addressData.CITY_AREA_2" />
      </div>

      <div class="col-12">
        <InputLabel label="dělení obcí – kód" />
        <ReadOnlyInput :value="addressData.CITY_AREA_3_CODE" />
      </div>
      <div class="col-12">
        <InputLabel
          label="dělení obcí – v ČR odpovídá správním obvodům – v Praze je to 'Praha 1' - 'Praha 22'"
        />
        <ReadOnlyInput :value="addressData.CITY_AREA_3" />
      </div>
    </div>
    <div v-if="cuzkData" class="row g-3 mt-3">
      <h2>Data z ČÚZK</h2>
      <div class="col-md-6">
        <InputLabel label="POU kód" />
        <ReadOnlyInput :value="cuzkData.pou.code" />
      </div>
      <div class="col-md-6">
        <InputLabel label="POU hodnota" />
        <ReadOnlyInput :value="cuzkData.pou.name" />
      </div>

      <div class="col-md-6">
        <InputLabel label="ORP kód" />
        <ReadOnlyInput :value="cuzkData.orp.code" />
      </div>
      <div class="col-md-6">
        <InputLabel label="ORP hodnota" />
        <ReadOnlyInput :value="cuzkData.orp.name" />
      </div>
    </div>

    <button
      v-if="addressData && cuzkData"
      type="button"
      class="mt-4 btn btn-primary"
      @click.prevent="submitAddressData"
    >
      Uložit
    </button>
  </template>
</template>
