<template>
	<div>
		<div class="top container">
			<header>
				<h1>Key-BNC</h1>
			</header>
			<nav>
				<div
					role="tablist"
					class="tab-nav"
				>
					<nav-button
						:is-selected="currentTab === Tab.MANAGE_CORPUS"
						@click="setTab(Tab.MANAGE_CORPUS)"
					>
						Manage Corpus
					</nav-button>
					<nav-button
						:is-selected="currentTab === Tab.WORD_STATS"
						@click="showStatsView"
					>
						Corpus Statistics
					</nav-button>
					<nav-button
						:is-selected="currentTab === Tab.ABOUT"
						@click="setTab(Tab.ABOUT)"
					>
						About
					</nav-button>
				</div>
			</nav>
		</div>
		<div class="tab-container container">
			<manage-corpus
				v-show="currentTab === Tab.MANAGE_CORPUS"
				:key-bnc="keyBnc"
				@corpus-changed="setDirty"
			/>
			<word-stats-view
				v-show="currentTab === Tab.WORD_STATS"
				:word-stats="wordStats"
			/>
			<about-view
				v-show="currentTab === Tab.ABOUT"
			/>
		</div>
	</div>
</template>

<script lang="ts">
import { defineComponent, PropType, reactive, toRefs } from 'vue'
import { KeyBnc } from 'key_bnc_wasm'
import { WordStats } from '../models'
import ManageCorpus from './ManageCorpus.vue'
import WordStatsView from './WordStats/WordStats.vue'
import NavButton from './buttons/NavButton.vue'
import AboutView from './About.vue'

const MAX_ITEMS = 1000

enum Tab {
	ABOUT,
	WORD_STATS,
	MANAGE_CORPUS,
}

export default defineComponent({
	components: {
		ManageCorpus,
		WordStatsView,
		NavButton,
		AboutView,
	},
	props: {
		keyBnc: {
			type: Object as PropType<KeyBnc>,
			required: true,
		},
	},
	setup (props) {
		const state = reactive({
			wordStats: [] as Array<WordStats>,
			currentTab: Tab.MANAGE_CORPUS,
			isDirty: false,
		})

		const setDirty = () => {
			state.isDirty = true
		}

		const updateStats = () => {
			const wordStats = (props.keyBnc.get_stats() as Array<WordStats>)
				.sort((a, b) => b.frequency - a.frequency)
			wordStats.splice(MAX_ITEMS)
			state.wordStats = wordStats
		}

		const showStatsView = () => {
			state.currentTab = Tab.WORD_STATS
			if (state.isDirty) {
				state.isDirty = false
				updateStats()
			}
		}

		return {
			...toRefs(state),
			setDirty,
			showStatsView,
			Tab,
			setTab (tab: Tab) {
				state.currentTab = tab
			},
		}
	},
})
</script>

<style lang="scss" scoped>
.top,
.tab-nav {
	display: flex;
	align-items: flex-end;
}

h1 {
	font-size: 1.1em;
	margin: 0 2rem 0 0;
	position: relative;
	top: 2rem;
	font-variant: small-caps;
	pointer-events: none;

	@media (max-width: 620px) {
		font-size: 0.8em;
		top: 0;
		margin: 1rem 0 0;
	}
}

.top {
	top: 0;
	left: 0;
	padding: 0;
	max-width: 100%;
	background-color: #000;
	color: #fff;
	font-size: 3em;
	height: 2.85em;

	@media (max-width: 620px) {
		height: auto;
		flex-direction: column;
		align-items: flex-start;
		justify-content: end;
	}
}

.container {
	padding-left: 1rem;
	padding-right: 1rem;
}

.tab-nav {
	position: relative;
	font-size: 1.5rem;
	font-weight: bold;
}

.tab-nav::before {
	position: absolute;
	content: " ";
	width: 100%;
	bottom: 0;
	left: 0;
	border-bottom: 1px solid black;
}
</style>
