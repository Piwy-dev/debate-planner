/**
 * @function vote - Sends a POST request to the server to vote on a topic and updates the vote count
 * @param {Event} event - The event that triggered the function
 * @returns {Promise} - The response from the server
 * @throws {Error} - If the response from the server is not ok
 */
async function vote(event) {
    const previousCount = document.querySelector(`.vote-count-${event.target.id}`).innerHTML;
    const topicId = event.target.id
    const voteType = event.target.classList.contains('upvote') ? 'upvote' : 'downvote';

    const response = await fetch(`/topics/${topicId}/vote/${voteType}`, {
        method: 'POST',
        form: {
            topic_id: topicId,
            vote_type: voteType
        }
    });

    // Toggle the vote button
    console.log(event.target.classList);
    if (event.target.classList.contains('voted')) {
        event.target.src = `/static/images/up_arrow_black.png`;
    } else {
        event.target.src = `/static/images/up_arrow_blue.png`;
    }

    // If the response is 200, update the vote count
    if (response === 200) {
        if (voteType === 'upvote') {
            const newCount = parseInt(previousCount) + 1;
            document.querySelector(`.vote-count-${event.target.id}`).innerHTML = newCount;
        } else {
            const newCount = parseInt(previousCount) - 1;
            document.querySelector(`.vote-count-${event.target.id}`).innerHTML = newCount;
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