<template>
	<div>
		<button @click="refresh">Generate wordso</button>

		<form
			@submit.prevent="
				(e) => {
					fetchData(e.target.elements.char.value);
				}
			"
		>
			<input name="char" />
		</form>
		<div v-if="words && words.all_words">
			{{ words.all_words.join(" ")
			}}<span v-for="char in words.all_words.join(' ')">{{
				char
			}}</span>
		</div>
	</div>
	<div><input v-model="model" style="all: unset; width: 100%" /></div>
	<div>
		<span v-for="c in model">{{ c }}</span>
	</div>
	<div>
		<span v-for="d in data">{{ d.key }}</span>
	</div>
	<input type="text" id="MasterInput" @keydown="watchKeydown" style="opacity: 0%; position: absolute;"/>
	<div @click="focusInput()" style="position: absolute; border: black 1px solid; height: 300px; width: 100%"></div>
	<div>{{ data }}</div>
	
</template>

<script setup>
const loading = ref(false);
const model = ref("");
const data = ref([]);
const wordsData = ref([])

const {
	data: words,
	refresh,
	pending,
	error,
} = await useAsyncData("words", async () => {
	return await $fetch("api/words");
});

async function fetchData(char = "") {
	const { data } = await useFetch(`api/words?char=${char.charAt(0)}`);
	words.value = data.value;
}

function focusInput(){
	document.getElementById('MasterInput').focus()
}

let finalKeydown = Date.now();

function watchKeydown(e) {
	e.preventDefault();
	e.stopImmediatePropagation();
	if (e.keyCode === 8 || e.keyCode === 46) {
		if (data.value.length) {
			data.value.pop();
		}
	} else if (e.keyCode >= 9 && e.keyCode <= 27) {
		console.log(e.key);
	} else {
		let key;
		if (e.key === "Enter") {
			key = "\n";
		} else {
			key = e.key;
		}
		const time = Date.now();
		data.value = [
			...data.value,
			{
				key: key,
				time: time,
				time_taken: (time - finalKeydown) / 1000,
			},
		];
		finalKeydown = time;
	}
}
</script>
