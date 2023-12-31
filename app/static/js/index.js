import { setDarkmode } from './darkmode.js';
import { setLanguage } from './language.js';
import { manageVotes } from './topics.js';

window.onload = function() {
    // Set the dark mode based on the user's preference
    setDarkmode();

    // Set the language based on the user's preference
    setLanguage();

    // Manage the vote buttons
    manageVotes();
};