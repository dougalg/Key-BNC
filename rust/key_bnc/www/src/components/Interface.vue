<template>
	<div>
		<nav class="tab-nav">
			<nav-button
				:is-selected="currentTab === tabs.MANAGE_CORPUS"
				@click.native="currentTab = tabs.MANAGE_CORPUS"
			>
				Manage Corpus
			</nav-button>
			<nav-button
				:is-selected="currentTab === tabs.WORD_STATS"
				@click.native="showStatsView"
			>
				View Statistics
			</nav-button>
		</nav>
		<div class="tab-container">
			<manage-corpus
				v-show="currentTab === tabs.MANAGE_CORPUS"
				:key-bnc="keyBnc"
				@corpus-changed="setDirty"
			/>
			<word-stats-view
				v-show="currentTab === tabs.WORD_STATS"
				:word-stats="wordStats"
			/>
		</div>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { KeyBnc } from '../../../pkg/key_bnc'
import ManageCorpus from './ManageCorpus.vue'
import WordStatsView from './WordStats.vue'
import NavButton from './NavButton.vue'

const MAX_ITEMS = 1000

interface WordStats {
	word: string;
	frequency: number;
	frequency_bnc: number;
	log_likelyhood: number;
	odds_ratio: number;
	dispersion: number;
}

const components = {
	ManageCorpus,
	WordStatsView,
	NavButton,
}

enum Tabs {
	WORD_STATS,
	MANAGE_CORPUS,
}

@Component({ components })
export default class Interface extends Vue {
	@Prop() private keyBnc!: KeyBnc
	private wordStats: Array<WordStats> = []
	private tabs = Tabs
	private currentTab: Tabs = Tabs.MANAGE_CORPUS
	private isDirty = false

	setDirty () {
		this.isDirty = true
	}

	showStatsView () {
		console.log('clicked')
		this.currentTab = Tabs.WORD_STATS
		if (this.isDirty) {
			this.isDirty = false
			this.updateStats()
		}
	}

	updateStats () {
		const wordStats = (this.keyBnc.get_stats() as Array<WordStats>)
			.sort((a, b) => b.frequency - a.frequency)
		wordStats.splice(MAX_ITEMS)
		this.wordStats = wordStats
	}
}
</script>

<style lang="scss" scoped>
.tab-nav {
	position: relative;
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
