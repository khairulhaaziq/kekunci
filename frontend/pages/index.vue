<template>
	<div class="p-10 max-w-7xl w-full">
		<h1 class="text-7xl font-bold mb-10">kekunci</h1>
		<div class="flex h-9 mb-6 shadow-sm w-fit">
			<button
				v-for="i in 26"
				:class="`font-medium border-y border-r w-9 border-neutral-400 flex-none flex items-center justify-center first:border-l first:rounded-l last:rounded-r ${
					currentChar ===
					String.fromCharCode(i + 96)
						? 'bg-neutral-500 text-white'
						: 'text-white/60'
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
		<div
			v-if="allData.length"
			:class="`fixed h-12 w-2 bg-[#3992FF] transition-all duration-100 ease-linear`"
			:style="`left: ${cursorLeft - 2}px; top: ${
				cursorTop + 6
			}px`"
		></div>
		<div
			@click="focusInput()"
			class="transition-all ease-linear duration-1000 mb-10 min-h-80 h-80 bg-neutral-800 pt-3 pb-4 px-6 rounded-xl w-full text-5xl leading-[54px]"
		>
			<template v-for="(word, index) in allData">
				<span
					:class="`ease-linear transition-opacity duration-1000 ${
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
								? 'bg-[#F44250] text-white opacity-100'
								: char.status ===
								  'error'
								? 'text-[#F44250] opacity-100'
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
						>{{
							char.character === " "
								? "\&nbsp"
								: char.character
						}}</span
					>
					<span
						:class="`${
							index ===
								currentWordNum -
									1 &&
							separator
								? 'cursor-key'
								: ''
						}`"
						>{{ " " }}</span
					></span
				>
			</template>
		</div>
		<input
			type="text"
			id="MasterInput"
			@keydown="watchKeydown"
			style="opacity: 0%; position: absolute"
		/>
		<div class="grid grid-cols-2 gap-6">
			<div>
				<div>
					<span v-for="d in typedData">{{
						d.key
					}}</span>
				</div>
				<div>{{ accArr }}</div>
				<div>{{ accuracies }}</div>
				<div>{{ totalTime }}</div>
			</div>
			<div>
				<!--<div class="border border-neutral-700 rounded-lg bg-neutral-900 h-96 overflow-scroll relative text-sm"><div class="grid grid-cols-6 py-4 px-6 border-b border-neutral-700 sticky top-0 bg-neutral-800/50 backdrop-blur-md"><div class="col-span-3">Character</div> <div class="col-span-1">Timing</div> <div class="col-span-2 text-right">Status</div></div><div v-for="data,index in flatData" class="grid grid-cols-6 py-4 px-8 odd:bg-neutral-800/30"><div class="col-span-1">{{ index+1 }}</div><div class="col-span-2">{{ data.character }}</div><div  class="col-span-1">{{ data.timing }}</div><div class="col-span-2 text-right">{{ data.status }}</div></div></div>-->
			</div>
		</div>
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
const currentIncorrect = ref(false);
const cursorLeft = ref(0);
const cursorTop = ref(0);
const totalTime = ref([]);
const flatData = computed(() => {
	return allData.value.flatMap((data) => {
		return data.characters;
	});
});
const accuracies = computed(() => {
	let initialValue = 0;
	let total_chars = 0;
	let correct_chars = 0;
	let error_chars = 0;
	const arr = allData.value.flatMap((data) => {
		return data.characters;
	});
	for (const d of arr) {
		initialValue += d.timing;
		d.status === "error"
			? error_chars++
			: d.status === "correct"
			? correct_chars++
			: "";
		total_chars++;
	}
	return {
		total_time: initialValue,
		total_chars,
		correct_chars,
		error_chars,
	};
});
const accArr = ref([]);
const startingTime = ref(0);

const {
	data: words,
	refresh,
	pending,
	error,
} = await useAsyncData("words", async () => {
	const { data } = await useFetch("api/words");
	return data.value;
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
	focusInput();
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
	} else if (
		(e.keyCode >= 9 && e.keyCode <= 27) ||
		(e.keyCode >= 91 && e.keyCode <= 93) ||
		(e.keyCode >= 112 && e.keyCode <= 183)
	) {
		console.log(e.key);
	} else {
		let key = e.key;
		const time = Date.now();
		typedData.value.length ? "" : (startingTime.value = time);
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
			if (
				currentPendingWordIndex.value !=
					currentCharNum.value ||
				currentIncorrect.value
			) {
				currentObj.status = "error";
				currentIncorrect.value = false;
			} else {
				currentObj.status = "correct";
			}
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
				totalTime.value.push(
					parseFloat(
						25 /
							((time -
								startingTime.value) /
								1000 /
								60)
					).toFixed(2)
				);
				accArr.value.push(
					(accuracies.value.correct_chars /
						accuracies.value.total_chars) *
						100
				);
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
			currentIncorrect.value = true;
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
		if (cursorKey?.getBoundingClientRect()) {
			const rect = cursorKey?.getBoundingClientRect();

			cursorLeft.value = parseFloat(rect.left);
			cursorTop.value = parseFloat(rect.top);
		}
		requestAnimationFrame(getCursorPosition);
	}

	requestAnimationFrame(getCursorPosition);
});
</script>
