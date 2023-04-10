<template>
	<div>
		<button @click="refresh">Generate wordso</button>
    <button @click="fetchData">Generate wordsso</button>

		<div v-if="!pending && words">{{ words.all_words ? words.all_words : words }}
    <div v-if="!loading">{{ wordsData.all_words }}</div>
    </div>

	</div>
</template>

<script setup>
const wordsData = ref({})
const loading = ref(false)

const {
	data: words,
	refresh,
	pending,
	error,
} = await useAsyncData("words", () => {
	const { data } = useFetch("http://127.0.0.1:5000/api/words");
	return data;
});

const fetchData = async()=>{
  loading.value = true
  const { data } = await useFetch("http://127.0.0.1:5000/api/words");
  wordsData.value = data 
  loading.value = false
}
</script>
