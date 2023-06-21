/**
 * @function vote - Sends a POST request to the server to vote on a topic
 * @param {Event} event - The event that triggered the function
 * @returns {Promise} - The response from the server
 */
function vote(event) {
    // Prevent the default action
    event.preventDefault();

    // Get the topic ID
    const topicId = event.target.dataset.topicId;

    // Get the vote type
    const voteType = event.target.dataset.voteType;

    // Send a POST request to the server
    return fetch(`/topics/${topicId}/vote`, {
        method: 'POST',
        body: JSON.stringify({
            voteType: voteType
        })
    })
    .then(response => response.json())
    .then(result => {
        // Update the vote count
        const voteCount = document.querySelector(`#vote-count-${topicId}`);
        voteCount.innerHTML = result.voteCount;
    }
    );
}

/**
 * @function manageVotes - Manages the vote buttons
 */
export function manageVotes() {
    const upvotes = document.querySelectorAll('.upvote');
    const downvotes = document.querySelectorAll('.downvote');
    
    // Add event listeners to the upvote buttons
    upvotes.forEach(upvote => {
        upvote.addEventListener('click', vote.bind(this)
        );
    });

    // Add event listeners to the downvote buttons
    downvotes.forEach(downvote => {
        downvote.addEventListener('click', vote.bind(this)
        );
    });
}