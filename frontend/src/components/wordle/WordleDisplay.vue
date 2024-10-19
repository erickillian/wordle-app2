<template>
    <v-card max-width="500" rounded="lg">
        <div class="wordle-container">
            <div class="wordle-alert-container" data-alert-container></div>
            <div data-guess-grid class="guess-grid">
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
                <div class="tile"></div>
            </div>
            <div data-keyboard class="keyboard">
                <button class="key" data-key="Q">Q</button>
                <button class="key" data-key="W">W</button>
                <button class="key" data-key="E">E</button>
                <button class="key" data-key="R">R</button>
                <button class="key" data-key="T">T</button>
                <button class="key" data-key="Y">Y</button>
                <button class="key" data-key="U">U</button>
                <button class="key" data-key="I">I</button>
                <button class="key" data-key="O">O</button>
                <button class="key" data-key="P">P</button>
                <div class="space"></div>
                <button class="key" data-key="A">A</button>
                <button class="key" data-key="S">S</button>
                <button class="key" data-key="D">D</button>
                <button class="key" data-key="F">F</button>
                <button class="key" data-key="G">G</button>
                <button class="key" data-key="H">H</button>
                <button class="key" data-key="J">J</button>
                <button class="key" data-key="K">K</button>
                <button class="key" data-key="L">L</button>
                <div class="space"></div>
                <button data-enter class="key large">Enter</button>
                <button class="key" data-key="Z">Z</button>
                <button class="key" data-key="X">X</button>
                <button class="key" data-key="C">C</button>
                <button class="key" data-key="V">V</button>
                <button class="key" data-key="B">B</button>
                <button class="key" data-key="N">N</button>
                <button class="key" data-key="M">M</button>
                <button data-delete class="key large">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                        <path fill="var(--color-tone-1)"
                            d="M22 3H7c-.69 0-1.23.35-1.59.88L0 12l5.41 8.11c.36.53.9.89 1.59.89h15c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H7.07L2.4 12l4.66-7H22v14zm-11.59-2L14 13.41 17.59 17 19 15.59 15.41 12 19 8.41 17.59 7 14 10.59 10.41 7 9 8.41 12.59 12 9 15.59z">
                        </path>
                    </svg>
                </button>
            </div>
        </div>
    </v-card>
</template>      


<script>
import { defineComponent, ref, watch } from 'vue';
import JSConfetti from 'js-confetti'

export default defineComponent({
    props: {
        wordLength: {
            type: Number,
            required: false,
            default: 5,
        },
        numGuesses: {
            type: Number,
            required: false,
            default: 6,
        },
        throwConfetti: {
            type: Boolean,
            required: false,
            default: false,
        },
        flipAnimationDelay: {
            type: Number,
            required: false,
            default: 150,
        },
        preventInput: {
            type: Boolean,
            required: true,
            default: false,
        },
        currentTiles: {
            type: String,
            required: true
        },
        correctTiles: {
            type: String,
            required: true,
        },
        onGuessSubmit: {
            type: Function,
            required: false,
        },
    },
    setup(props) {
        const currentGuess = ref('');
        const currentRow = ref(0);
        const animateNextTileChange = ref(false);

        const correctMap = {
            0: "wrong",
            1: "wrong-location",
            2: "correct",
        }

        // Adds current guess letters by watching for changes in the current guess ref
        // Also handles the animation for the added tiles
        watch(currentGuess, (newGuess, oldGuess) => {
            // Update the tiles with the new letters in the current guess using the current row
            const guess = newGuess.padEnd(props.wordLength, '');
            const currentRowTiles = getCurrentRowTiles();
            currentRowTiles.forEach((tile, index) => {
                if (guess[index] !== oldGuess[index]) {
                    tile.textContent = guess[index];
                    if (guess[index] !== '' && guess[index] !== undefined) {
                        tile.classList.add("pop"); // Add pop animation
                        tile.addEventListener("animationend", () => {
                            tile.classList.remove("pop");
                        }, { once: true });
                    }
                }
            });
        });

        // watch for changes in currentTiles or correctTiles and update the tiles accordingly
        // also handle the flipping animation for the tiles if more tiles are added
        watch(() => props.currentTiles, (newTiles, oldTiles) => {
            const tilesToFlip = [];
            for (let i = 0; i < newTiles.length; i++) {
                if (newTiles[i] !== oldTiles[i] && newTiles[i] !== '' && newTiles[i] !== undefined) {
                    tilesToFlip.push(i);
                }
            }
            updateTiles(tilesToFlip);
        });

        // If the preventInput prop changes to true, clear the current guess
        watch(() => props.preventInput, (newVal) => {
            if (newVal && currentGuess.value.length !== props.wordLength) {
                currentGuess.value = '';
            }
        });

        const getCurrentRowTiles = () => {
            const tiles = document.querySelectorAll('.tile');
            return Array.from(tiles).slice((currentRow.value-1) * props.wordLength, currentRow.value * props.wordLength);
        };

        const clearTiles = () => {
            const tiles = document.querySelectorAll('.tile');
            tiles.forEach((tile) => {
                tile.textContent = '';
                tile.dataset.letter = '';
                tile.dataset.state = '';
            });
        }

        const animateNextTiles = () => {
            animateNextTileChange.value = true;
        };
        
        // Handles key presses / button clicks and updates the current guess
        const handleKey = (key) => {
            // console.log(props.preventInput, currentRow.value <= props.numGuesses);
            if (props.preventInput || currentRow.value <= props.numGuesses) return;
            
            if (key === 'enter') {
                submitGuess();
            } else if (key === 'backspace') {
                currentGuess.value = currentGuess.value.slice(0, -1);
            } else if (currentGuess.value.length < props.wordLength && key.match(/^[A-Za-z]$/)) {
                currentGuess.value += key;
            }
        };

        const simulateKey = (key) => {
            if(currentGuess.value.length < props.wordLength && key.match(/^[A-Za-z]$/)) {
                currentGuess.value += key;
            }
        };

        const showAlert = (message) => {
            const alertContainer = document.querySelector("[data-alert-container]");

            const alert = document.createElement("div"); // get the empty alert div
            alert.textContent = message; // add message
            alert.classList.add("wordle-alert"); // add alert class

            if (alertContainer) {
                alertContainer.prepend(alert);
            }
            const DELAY = 1000; // Set the delay value in milliseconds
            setTimeout(() => {
                alert.style.transition = 'opacity 0.5s'; // Add transition for fading effect
                alert.style.opacity = '0'; // Fade out the alert
                setTimeout(() => {
                    alert.remove(); // Remove the alert after fading out
                }, 500); // Adjust the delay for the fade out animation
            }, DELAY);
        };

        const spinLastRow = () => {
            const tiles = document.querySelectorAll('.tile');
            const lastRowTiles = Array.from(tiles).slice((currentRow.value - 2) * props.wordLength, (currentRow.value-1) * props.wordLength);

            lastRowTiles.forEach((tile) => {
                tile.classList.add('twirl'); // Add spin animation
            });

            setTimeout(() => {
                lastRowTiles.forEach((tile) => {
                    tile.classList.remove('twirl');
                });
            }, 8000); // Adjust the delay for the spin animation to finish

            if (props.throwConfetti) {
                const jsConfetti = new JSConfetti()
                jsConfetti.addConfetti({
                    confettiNumber: 500,
                    confettiColors: [
                        '#3876bc', '#ffffff',
                    ],
                });
            }
        };

        const shakeGuess = () => {
            const currentRowTiles = getCurrentRowTiles();
            currentRowTiles.forEach((tile) => {
                tile.classList.add('shake'); // Add shake animation
                tile.addEventListener('animationend', () => {
                    tile.classList.remove('shake');
                }, { once: true });
            });
        };

        // Submits the current guess to the parent component by calling the onGuessSubmit function
        const submitGuess = throttle(() => {
            if (currentGuess.value.length !== props.wordLength) return;
            // submit the guess to the parent component
            if (props.onGuessSubmit) {
            props.onGuessSubmit(currentGuess.value);
            animateNextTileChange.value = true;
            }
        }, 500); // Adjust the throttle delay to 500 milliseconds

        // Throttle function to prevent multiple guesses from getting submitted within 0.5 seconds
        function throttle(func, limit) {
            let inThrottle;
            return function(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
            };
        }

        // Updates the tiles with the current
        const updateTiles = (tilesToFlip) => {
            // Determine the current row
            currentRow.value = Math.floor(props.currentTiles.length / props.wordLength)+1;
            currentGuess.value = '';

            // Gets all tiles and keys
            const tiles = document.querySelectorAll('.tile');
            const keys = document.querySelectorAll('.key');
            const dataKeyboard = document.querySelector('[data-keyboard]');

            // gets all the current tiles and correct tiles
            const currentTiles = props.currentTiles.split('');
            const correctTiles = props.correctTiles.split('');

            // Iterate through all letters and update the keyboard.  First color all wrong letters, then work up to correct letters
            keys.forEach((key) => {
                key.classList.remove('wrong', 'wrong-location', 'correct');
            });
            for (let j = 0; j < Object.keys(correctMap).length; j++) {
                for (let i = 0; i < currentTiles.length; i++) {
                    const letter = currentTiles[i].toLowerCase();
                    const correct = Number(correctTiles[i]);

                    if (correct === j) {
                        const key = dataKeyboard.querySelector(`[data-key="${letter}"i]`); // get each key - the i makes it case insensitive
                        key?.classList.add(correctMap[j] || '');
                    }
                }
            }
            
            // Function to set a tiles state and letter
            const setTileState = (tile, correct, letter) => {
                tile.textContent = letter;
                tile.dataset.letter = letter;
                tile.dataset.state = correctMap[correct] || '';
            };
            
            // Get the current tiles and display them, 
            // also handle the flipping animation
            let flipIndex = 0;
            tiles.forEach((tile, index) => {
                const letter = currentTiles[index];
                const correct = correctTiles[index];

                if (tilesToFlip.includes(index) && animateNextTileChange.value) {
                    setTimeout(() => {
                        tile.classList.add('flip');
                        setTileState(tile, correct, letter);
                        setTimeout(() => {
                            tile.classList.remove('flip');
                        }, props.flipAnimationDelay);
                    }, flipIndex * props.flipAnimationDelay);
                    flipIndex++;
                } else {
                    setTileState(tile, correct, letter);
                }
            });
            
            // check if the last row is all correct and if so bounce all tiles and then spin the last row
            const last_tiles = props.correctTiles.slice(-props.wordLength);
            if (last_tiles === '2'.repeat(props.wordLength) && animateNextTileChange.value) {
                const flipTotalTime = (flipIndex) * props.flipAnimationDelay;
                setTimeout(() => {
                    const allTiles = document.querySelectorAll('.tile');
                    allTiles.forEach((tile, index) => {
                        if (tile.textContent.trim() !== '') { // Only bounce non-empty tiles
                            setTimeout(() => {
                                tile.classList.add('bounce');
                                tile.addEventListener('animationend', () => {
                                    tile.classList.remove('bounce');
                                }, { once: true });
                            }, index * 30); // Adjust the delay for the bounce animation
                        }
                    });

                    setTimeout(() => {
                        spinLastRow();
                    }, allTiles.length * 30 + 400); // Adjust the delay for the bounce animation to finish
                }, flipTotalTime);
            }
            animateNextTileChange.value = false;
        };

        // Add event listener for keydown event and for key press on buttons
        onMounted(() => {
            updateTiles([]);

            document.addEventListener('keydown', (e) => {
                handleKey(e.key.toLowerCase());
            });
            const buttons = document.querySelectorAll('.key:not([data-enter]):not([data-delete])');
            buttons.forEach((button) => {
                button.addEventListener('click', (e) => {
                    const key = e.target.dataset.key.toLowerCase();
                    handleKey(key);
                });
            });
            const enterButton = document.querySelector('[data-enter]');
            enterButton.addEventListener('click', () => {
                handleKey('enter');
            });
            const deleteButton = document.querySelector('[data-delete]');
            deleteButton.addEventListener('click', () => {
                handleKey('backspace');
            });
        });

        // remove event listeners on unmount
        onUnmounted(() => {
            document.removeEventListener('keydown', (e) => {
                handleKey(e.key);
            });
            const buttons = document.querySelectorAll('.key:not([data-enter]):not([data-delete])');
            buttons.forEach((button) => {
                button.removeEventListener('click', (e) => {
                    const key = e.target.dataset.key; // Add null checks
                    handleKey(key);
                });
            });
            const enterButton = document.querySelector('[data-enter]');
            if (enterButton) { // Add null check
                enterButton.removeEventListener('click', () => {
                    handleKey('Enter');
                });
            }
            const deleteButton = document.querySelector('[data-delete]');
            if (deleteButton) { // Add null check
                deleteButton.removeEventListener('click', () => {
                    handleKey('Backspace');
                });
            }
        });
        // Return the reactive variables and functions that will be used in the component
        return {
            currentGuess, // The current guess entered by the user
            currentRow, // The current row in the guess grid
            showAlert, // A function to display an alert message
            spinLastRow, // A function to spin the last row and throw confetti
            shakeGuess, // A function to shake the current guess tiles
            simulateKey, // A function to simulate a key press
            animateNextTiles, // A function to animate the next row of tiles
        };
    }
});
</script>

<!-- // import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
// import { useWordleStore } from '../stores/wordle';

// // CONSTANTS
// const WORD_LENGTH = 5;
// const FLIP_ANIMATION_DELAY = 300;
// const FLIP_ANIMATION_LENGTH = 300;
// const BOUNCE_ANIMATION_DELAY = 30;
// const BOUNCE_ANIMATION_LENGTH = 400;
// const TWIRL_ANIMATION_DELAY = 0;
// const TWIRL_ANIMATION_LENGTH = 1500;
// const DANCE_ANIMATION_DELAY = 50;
// const ANIMATION_LENGTH = 500;

// const store = useWordleStore();

// const guessGrid = ref(null);
// const keyboard = ref(null);
// const alertContainer = ref(null);

// onMounted(async () => {
//     guessGrid.value = document.querySelector("[data-guess-grid]");
//     keyboard.value = document.querySelector("[data-keyboard]");
//     alertContainer.value = document.querySelector("[data-alert-container]");
//     await store.getWordleStatus();
//     startInteraction();
// });

// onUnmounted(() => {
//     stopInteraction();
//     guessGrid.value = null;
//     keyboard.value = null;
//     alertContainer.value = null;
// });

// const startInteraction = () => {
//   document.addEventListener("click", handleMouseClick);
//   document.addEventListener("keydown", handleKeyPress);
// };

// const stopInteraction = () => {
//   document.removeEventListener("click", handleMouseClick);
//   document.removeEventListener("keydown", handleKeyPress);
// };

// const closeWinOverlay = () => {
//   winOverlay.value = false;
// };

// const handleMouseClick = (e) => {
//     if (e.target.matches("[data-key")) {
//         // if event target is a key, press that key
//         addLetter(e.target.dataset.key.toLowerCase());
//     }
//     else if (e.target.matches("[data-enter]")) { 
//         // if user clicks enter, submit the guess
//         submitGuess();
//     }
//     else if (e.target.matches("[data-delete]") || e.target.parentElement.matches("[data-delete]") || e.target.parentElement.parentElement.matches("[data-delete]")) {
//          // if user clicks delete, remove that key
//         deleteLetter();
//     }
// };

// const handleKeyPress = (e) => {
//     if (e.key === "Enter") { // if the key is enter, submit guess
//         submitGuess()
//         return
//     }
//     else if (e.key === "Backspace" || e.key === "Delete") { // if user presses backspace or delete, delete key
//         deleteLetter()
//     }
//     else if (e.key.match(/^[a-z]$/)) { // regex for one single letter between a and z
//         addLetter(e.key.toLowerCase());
//     }
// };

// const addLetter = (letter) => {
//     if (inputs.value.guess.length >= WORD_LENGTH) return; // if the guess is already 5 letters, return

//     addLetterGUI(letter); // add the letter to the GUI
//     inputs.value.guess += letter; // add the letter to the guess
// }

// const deleteLetter = () => {
//     if (inputs.value.guess.length == 0) return; // if the guess is already 5 letters, return
//     deleteLetterGUI(); // delete the last letter from the GUI
//     inputs.value.guess = inputs.value.guess.slice(0, -1); // remove the last letter from the guess
// };


// const addLetterGUI = (letter) => {
//     const activeTiles = getActiveTiles(); // get array of active tiles
//     if (activeTiles.length >= WORD_LENGTH) return; // make sure that user cannot keep typing after 5 letters

//     const nextTile = guessGrid.value.querySelector(":not([data-letter])"); // returns the first tile that doesn't have a value
//     nextTile.dataset.letter = letter; // add the letter to the tile's dataset
//     nextTile.textContent = letter; // make the html the key
//     nextTile.dataset.state = "active"; // set it to active
//     nextTile.classList.add("pop");
//     nextTile.addEventListener(
//         "animationend",
//         () => {
//             nextTile.classList.remove("pop");
//         },
//         { once: true }
//     );
// };

// const deleteLetterGUI = () => {
//     const activeTiles = getActiveTiles(); // get array of active tiles
//     const lastTile = activeTiles[activeTiles.length - 1]; // get the last active tile

//     if (lastTile) {
//         lastTile.removeAttribute("data-letter"); // remove the letter from the tile's dataset
//         lastTile.textContent = ""; // remove the letter from the html
//         lastTile.dataset.state = ""; // set the state to empty
//     }
// };

// const getActiveTiles = () => {
//     return guessGrid.value.querySelectorAll('[data-state="active"]');
// };

// const getFilledTiles = () => {
//     return guessGrid.value.querySelectorAll('[data-letter]');
// };

// const submitGuess = () => {
//     stopInteraction()
//     const activeTiles = [...getActiveTiles()] // get the array of active tiles
//     if (activeTiles.length !== WORD_LENGTH) { // if the guess isn't long enough, can't submit it!
//         showAlert("Not enough letters!")
//         shakeTiles(activeTiles)
//         startInteraction()
//         return
//     }
//     const guess = activeTiles.reduce((word, tile) => { // sum the array of individual letters into a string
//         return word + tile.dataset.letter
//     }, "") // returns a string

//     if (guessed == false) {
//         store.makeGuess({ guess: guess });
//         guessed = true;
//     }
    
//     // activeTiles.forEach((...params) => this.flipTile(...params, guess)) // flip tile animation
// };

// const initialGuesses = () => {
//     if (store.status_loading == false) {
//         const guess_history = store.wordle.guess_history;
//         const correct = store.wordle.correct;
//         console.log(store.wordle.guess_history)
//         console.log(store.wordle.correct)

//         for (var i=0; i < guess_history.length; i++) {
//             const nextTile = guessGrid.value.querySelector(":not([data-letter])");
//             const letter = guess_history[i].toLowerCase()
//             nextTile.textContent = letter
//             nextTile.dataset.letter = letter
//             const key = keyboard.value.querySelector(`[data-key="${letter}"i]`) 
//             if (key) {
//                 if (correct[i] == "0") {
//                     nextTile.dataset.state = "wrong"
//                     key.classList.add("wrong")
//                 }
//                 if (correct[i] == "1") {
//                     nextTile.dataset.state = "wrong-location"
//                     key.classList.add("wrong-location")
//                 }
//                 if (correct[i] == "2") {
//                     nextTile.dataset.state = "correct"
//                     key.classList.add("correct")
//                 }
//             }
//         }
//         var time = bounceTiles();
//         setTimeout(() => {
//             checkWinLose()
//         }, time);
//     } else {
//         console.log("wordle is still loading")
//     }
// };

// const checkInteraction = () => {
//   if (wordle.solved) {
//     stopInteraction();
//     winOverlay.value = true;
//   } else {
//     startInteraction();
//   }
// };

// const checkWinLose = () => {
//   if (wordle.solved) {
//     stopInteraction();
//     winOverlay.value = true;
//     // Implement win animation
//   } else if (wordle.value.guess_history.split(',').length >= 6) {
//     stopInteraction();
//     // Implement lose scenario
//   }
// };

// const showAlert = (message, DELAY = 1000) => {
//     const alert = document.createElement("div"); // get the empty alert div
//     alert.textContent = message; // add message
//     alert.classList.add("alert"); // add the alert class
//     if (DELAY == null) return;
//     setTimeout(() => {
//         console.log("hiding alert");
//         alert.classList.add("hide");
//         alert.addEventListener("transitionend", () => {
//             alert.remove();
//         }, { once: true });
//     }, DELAY);
//     alertContainer.value.prepend(alert);
// };

// const shakeTiles = (tiles) => {
//     tiles.forEach(tile => {
//         tile.classList.add("shake")
//         tile.addEventListener("animationend", () => {
//             tile.classList.remove("shake")
//         }, { once: true })
//     })
// };

// const danceTiles = (tiles) => {
//     tiles.forEach((tile, index) => {
//         setTimeout(() => {
//             tile.classList.add("dance")
//             tile.addEventListener(
//                 "animationend",
//                 () => {
//                     tile.classList.remove("dance")
//                 },
//                 { once: true }
//             )
//         }, (index * DANCE_ANIMATION_DELAY))
//     })
// };

// const bounceTiles = () => {
//     const allTiles = getFilledTiles();
//     for (let i = 0; i < allTiles.length; i++) {
//         const tile = allTiles[i]
//         setTimeout(() => {
//             tile.classList.add("bounce")
//             tile.addEventListener(
//                 "animationend",
//                 () => {
//                     tile.classList.remove("bounce")
//                 },
//                 { once: true }
//             )
//         }, (i * BOUNCE_ANIMATION_DELAY))
        
//     }
//     return (allTiles.length*BOUNCE_ANIMATION_DELAY+BOUNCE_ANIMATION_LENGTH)
// };

// const twirlWinningTiles = () => {
//     var time = 0;
//     const allTiles = getFilledTiles();
//     for (let i = allTiles.length-WORD_LENGTH; i < allTiles.length; i++) {
//         const tile = allTiles[i]
//         setTimeout(() => {
//             tile.classList.add("twirl")
//             tile.classList.add("rainbow");
//             tile.addEventListener(
//                 "animationend",
//                 () => {
//                     tile.classList.remove("twirl")
//                 },
//                 { once: true }
//             )
//         }, (i * TWIRL_ANIMATION_DELAY))
//         time += TWIRL_ANIMATION_DELAY;
//     }
//     return (WORD_LENGTH*BOUNCE_ANIMATION_DELAY+BOUNCE_ANIMATION_LENGTH)
// };
// </script> -->

<style scoped src="./WordleDisplay.css" >
</style>