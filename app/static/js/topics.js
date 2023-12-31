/**
 * @function vote - Sends a POST request to the server to vote on a topic and updates the vote count
 * @param {Event} event - The event that triggered the function
 * @returns {Promise} - The response from the server
 * @throws {Error} - If the response from the server is not ok
 */
async function vote(event) {
    const topicId = event.target.id
    const voteType = event.target.classList.contains('upvote') ? 'upvote' : 'downvote';

    const response = await fetch(`/topics/${topicId}/vote/${voteType}`, {
        method: 'POST',
        form: {
            topic_id: topicId,
            vote_type: voteType
        }
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        const topic = await response.json();
        const voteCount = document.querySelector(`.vote-count-${topicId}`);

        voteCount.innerHTML = topic.votes;

        if (topic.vote_type === 'upvote') {
        }
    }
}


/**
 * @function manageVotes - Manages the vote buttons
 */
export function manageVotes() {
    const upvotes = document.querySelectorAll('.upvote');
    const downvotes = document.querySelectorAll('.downvote');
    
    // Add event listeners to the upvote buttons
    upvotes.forEach(upvote => {
        upvote.addEventListener('click', vote.bind(this), false);
    });

    // Add event listeners to the downvote buttons
    downvotes.forEach(downvote => {
        downvote.addEventListener('click', vote.bind(this), false);
    });
}