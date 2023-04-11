<template>
	<div class="p-10 max-w-3xl">
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
		<div class="flex border-l h-9 mb-3">
			<button
				v-for="i in 26"
				:class="`font-medium border-y border-r w-9 flex-none flex items-center justify-center ${
					currentChar ===
					String.fromCharCode(i + 96)
						? 'bg-black text-white'
						: 'text-black/60'
				}`"
				@click="
					(e) => {
						fetchData(
							e.target.textContent.toLowerCase()
						);
					}
				"
			>
				{{ String.fromCharCode(i + 64) }}
			</button>
		</div>
		<div v-if="allData.length" :class="`fixed h-12 w-1 bg-blue-500 transition-all duration-100`" :style="`left: ${cursorLeft}px; top: ${cursorTop + 6}px`"
						></div
					>
		<div
			v-if="allData.length"
			@click="focusInput()"
			class="mb-10 min-h-40 bg-gray-50 py-3 w-full text-5xl leading-[54px]"
		>
			<template v-for="(word, index) in allData">
				<span
					:class="`${
						index === currentWordNum &&
						separator
							? 'relative'
							: ''
					}`"
					><span
						v-for="(
							char, charIndex
						) in word.characters"
						:class="` ${
							char.status ===
							'correct'
								? 'opacity-100'
								: char.status ===
								  'extra'
								? 'bg-red-500 text-white opacity-100'
								: char.status ===
								  'error'
								? 'text-red-500 opacity-100'
								: 'opacity-50'
						} ${
							index ===
								currentWordNum &&
							charIndex ===
								currentPendingWordIndex &&
							!separator
								? 'cursor-key'
								: ''
						}`"
						>{{ char.character === ' ' ? '\&nbsp' : char.character }}</span>
					<span :class="`${index === currentWordNum-1 && separator ? 'cursor-key': ''}`">{{ " " }}</span></span
				>
			</template>
		</div>

		<div>
			<input
				v-model="model"
				style="all: unset; width: 100%"
			/>
		</div>
		<div>
			<span v-for="c in model">{{ c }}</span>
		</div>
		<div>
			<span v-for="d in typedData">{{ d.key }}</span>
		</div>
		<input
			type="text"
			id="MasterInput"
			@keydown="watchKeydown"
			style="opacity: 0%; position: absolute"
		/>
	</div>
</template>

<script setup>
const loading = ref(false);
const model = ref("");
const typedData = ref([]);
const wordsData = ref([]);
const currentChar = ref("");
const allData = ref([]);
const currentWordNum = ref(0);
const currentCharNum = ref(0);
const currentPendingWordIndex = ref(0);
const separator = ref(false);
const cursorLeft = ref(0);
const cursorTop = ref(0);

const {
	data: words,
	refresh,
	pending,
	error,
} = await useAsyncData("words", async () => {
	const {data} = await useFetch("api/words");
	return data.value
});

async function fetchData(char = "") {
	if (char) {
		currentChar.value = char.charAt(0);
	} else {
		char = currentChar.value;
	}
	typedData.value = [];
	allData.value = [];
	resetIndexes();
	const { data } = await useFetch(
		`api/words?char=${currentChar.value.charAt(0)}`
	);
	words.value = data.value;
	data.value.all_words.map((i) => {
		const characters = i.split("");
		const charData = [];
		for (const char of characters) {
			charData.push({
				character: char,
				timing: 0,
				status: "pending",
			});
		}

		allData.value.push({ word: i, characters: charData });
	});
	focusInput()
}

function resetIndexes() {
	currentWordNum.value = 0;
	currentCharNum.value = 0;
	currentPendingWordIndex.value = 0;
	separator.value = false;
}

function focusInput() {
	document.getElementById("MasterInput").focus();
}

let finalKeydown = Date.now();

function watchKeydown(e) {
	e.preventDefault();
	e.stopImmediatePropagation();
	if (e.key === "Enter") {
		typedData.value = [];
		fetchData();
	} else if (e.keyCode === 8 || e.keyCode === 46) {
		if (typedData.value.length) {
			typedData.value.pop();
		}
		if (
			allData.value.length &&
			allData.value[currentWordNum.value].characters[
				currentPendingWordIndex.value - 1
			].status === "extra"
		) {
			allData.value[currentWordNum.value].characters.splice(
				currentPendingWordIndex.value - 1,
				1
			);
			currentPendingWordIndex.value--;
		}
	} else if (e.keyCode >= 9 && e.keyCode <= 27) {
		console.log(e.key);
	} else {
		let key = e.key;
		const time = Date.now();
		typedData.value = [
			...typedData.value,
			{
				key: key,
				time: time,
				time_taken: typedData.value.length
					? (time - finalKeydown) / 1000
					: 0,
			},
		];
		console.log(e.key);
		if (separator.value && e.key === " ") {
			separator.value = !separator.value;
		} else if (
			allData.value.length &&
			allData.value[currentWordNum.value].characters[
				currentPendingWordIndex.value
			].character === e.key &&
			!separator.value
		) {
			function deleteExtras() {
				let totalExtras =
					currentPendingWordIndex.value -
					currentCharNum.value;
				allData.value[
					currentWordNum.value
				].characters.splice(
					currentCharNum.value,
					totalExtras
				);
			}
			deleteExtras();
			const currentObj =
				allData.value[currentWordNum.value].characters[
					currentCharNum.value
				];
			currentPendingWordIndex.value != currentCharNum.value
				? (currentObj.status = "error")
				: (currentObj.status = "correct");
			currentObj.timing =
				currentWordNum.value + currentCharNum.value == 0
					? 0
					: (time - finalKeydown) / 1000;
			if (
				allData.value.length ===
					currentWordNum.value + 1 &&
					allData.value[currentWordNum.value].characters
					.length ===
				currentCharNum.value + 1
			) {
				fetchData(currentChar.value);
			} else if (
				allData.value[currentWordNum.value].characters
					.length ===
				currentCharNum.value + 1
			) {
				currentWordNum.value++;
				currentCharNum.value = 0;
				separator.value = true;
			} else currentCharNum.value++;
			currentPendingWordIndex.value = currentCharNum.value;
		} else if (allData.value.length) {
			allData.value[currentWordNum.value].characters.splice(
				currentPendingWordIndex.value,
				0,
				{ character: e.key, timing: 0, status: "extra" }
			);
			currentPendingWordIndex.value++;
		}
		finalKeydown = time;
	}
}

onMounted(() => {
	function getCursorPosition() {
		const cursorKey = document.querySelector(".cursor-key");
		if(cursorKey?.getBoundingClientRect()){
		const rect = cursorKey?.getBoundingClientRect();

		console.log(rect.left)
		console.log(rect.top)
		cursorLeft.value = parseFloat(rect.left)
		cursorTop.value = parseFloat(rect.top)
		}
		requestAnimationFrame(getCursorPosition);
	}

	requestAnimationFrame(getCursorPosition);
});
</script>
