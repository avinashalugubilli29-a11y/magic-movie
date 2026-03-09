/* ============================================================
   Movie Magic — movies1.js
   Handles: filter buttons, seat selection, booking summary
   ============================================================ */

// ─── Run everything when the DOM is ready ───
document.addEventListener("DOMContentLoaded", function () {

  // Each init function checks if its elements exist
  // so this single file is safely included on every page.

  initMovieFilters();
  initSeatPicker();
  initShowtimeSelector();
  autoHideFlash();
});


// ─────────────────────────────────────────────────────────
//  MOVIE FILTER BUTTONS  (home.html)
// ─────────────────────────────────────────────────────────

function initMovieFilters() {
  const filterBtns  = document.querySelectorAll(".filter-btn");
  const movieCards  = document.querySelectorAll(".movie-card");

  if (!filterBtns.length) return; // Not on the home page

  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const genre = btn.getAttribute("data-genre"); // e.g. "All", "Sci-Fi"

      // Update active button
      filterBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");

      // Show / hide cards based on genre
      movieCards.forEach(function (card) {
        const cardGenre = card.getAttribute("data-genre");
        if (genre === "All" || cardGenre === genre) {
          card.style.display = "flex";
          card.style.animation = "fadeUp 0.3s ease both";
        } else {
          card.style.display = "none";
        }
      });
    });
  });
}


// ─────────────────────────────────────────────────────────
//  SEAT PICKER  (tickets.html)
// ─────────────────────────────────────────────────────────

function initSeatPicker() {
  const seatGrid  = document.getElementById("seat-grid");
  if (!seatGrid) return; // Not on tickets page

  const seats         = seatGrid.querySelectorAll(".seat:not(.seat-taken)");
  const selectedInput = document.getElementById("selected-seats-input"); // hidden input
  const countEl       = document.getElementById("seat-count");
  const totalEl       = document.getElementById("total-price");
  const seatsDisplay  = document.getElementById("seats-display");
  const pricePerTicket = parseFloat(seatGrid.getAttribute("data-price") || "0");

  let selected = []; // Array of seat IDs like ["A1", "B3"]

  seats.forEach(function (seat) {
    seat.addEventListener("click", function () {
      const seatId = seat.getAttribute("data-seat");

      if (seat.classList.contains("seat-selected")) {
        // Deselect the seat
        seat.classList.remove("seat-selected");
        selected = selected.filter(function (s) { return s !== seatId; });
      } else {
        // Select the seat
        seat.classList.add("seat-selected");
        selected.push(seatId);
      }

      updateBookingSummary();
    });
  });

  // Update the booking summary panel with current selection
  function updateBookingSummary() {
    const count = selected.length;
    const total = (count * pricePerTicket).toFixed(2);

    // Update count and total
    if (countEl)  countEl.textContent  = count;
    if (totalEl)  totalEl.textContent  = "₹" + Math.round(count * pricePerTicket);

    // Update displayed seat tags
    if (seatsDisplay) {
      seatsDisplay.innerHTML = "";
      if (selected.length === 0) {
        seatsDisplay.innerHTML = '<span style="color:var(--text-muted);font-size:0.85rem">None selected yet</span>';
      } else {
        selected.forEach(function (s) {
          const tag = document.createElement("span");
          tag.className = "seat-tag";
          tag.textContent = s;
          seatsDisplay.appendChild(tag);
        });
      }
    }

    // Keep the hidden form input in sync (seats submitted as checkboxes)
    syncHiddenInputs();
  }

  // Sync selected seats with hidden checkbox inputs for form submission
  function syncHiddenInputs() {
    // Remove any previously created hidden inputs
    const old = document.querySelectorAll(".dynamic-seat-input");
    old.forEach(function (el) { el.remove(); });

    // Create a hidden input for each selected seat
    const form = document.getElementById("booking-form");
    if (!form) return;

    selected.forEach(function (seatId) {
      const input  = document.createElement("input");
      input.type   = "hidden";
      input.name   = "seats";
      input.value  = seatId;
      input.className = "dynamic-seat-input";
      form.appendChild(input);
    });
  }

  // Initial render
  updateBookingSummary();
}


// ─────────────────────────────────────────────────────────
//  SHOWTIME SELECTOR  (tickets.html)
// ─────────────────────────────────────────────────────────

function initShowtimeSelector() {
  const showtimeBtns = document.querySelectorAll(".showtime-btn");
  const showtimeInput = document.getElementById("showtime-input");
  const movieId       = document.getElementById("movie-id-value");

  if (!showtimeBtns.length) return;

  showtimeBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      // Update active button
      showtimeBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");

      const showtime = btn.getAttribute("data-time");

      // Update the hidden form field
      if (showtimeInput) showtimeInput.value = showtime;

      // Fetch booked seats for the new showtime via AJAX
      if (movieId) {
        fetchBookedSeats(movieId.value, showtime);
      }

      // Clear currently selected seats when changing showtime
      clearSelectedSeats();
    });
  });
}

// Fetch booked seats from the server for a given theatre + showtime
function fetchBookedSeats(movieId, showtime) {
  const theatreEl  = document.getElementById("theatre-input");
  const theatre_id = theatreEl ? theatreEl.value : "";
  const url = "/api/booked_seats?movie_id=" + encodeURIComponent(movieId)
            + "&theatre_id=" + encodeURIComponent(theatre_id)
            + "&showtime="   + encodeURIComponent(showtime);

  fetch(url)
    .then(function (res) { return res.json(); })
    .then(function (data) {
      updateTakenSeats(data.booked || []);
    })
    .catch(function (err) {
      console.warn("Could not fetch booked seats:", err);
    });
}

// Mark seats as taken / available based on server response
function updateTakenSeats(bookedList) {
  const allSeats = document.querySelectorAll(".seat");
  allSeats.forEach(function (seat) {
    const id = seat.getAttribute("data-seat");
    if (bookedList.includes(id)) {
      seat.classList.add("seat-taken");
      seat.classList.remove("seat-selected");
    } else {
      seat.classList.remove("seat-taken");
    }
  });
}

// Deselect all seats (e.g. when changing showtime)
function clearSelectedSeats() {
  const selected = document.querySelectorAll(".seat-selected");
  selected.forEach(function (s) { s.classList.remove("seat-selected"); });

  // Also update summary
  const countEl   = document.getElementById("seat-count");
  const totalEl   = document.getElementById("total-price");
  const displayEl = document.getElementById("seats-display");

  if (countEl)   countEl.textContent  = "0";
  if (totalEl)   totalEl.textContent  = "$0.00";
  if (displayEl) displayEl.innerHTML  = '<span style="color:var(--text-muted);font-size:0.85rem">None selected yet</span>';

  // Clear hidden inputs
  document.querySelectorAll(".dynamic-seat-input").forEach(function (el) { el.remove(); });
}


// ─────────────────────────────────────────────────────────
//  AUTO-HIDE FLASH MESSAGES
// ─────────────────────────────────────────────────────────

function autoHideFlash() {
  const flashMessages = document.querySelectorAll(".flash");
  flashMessages.forEach(function (msg) {
    setTimeout(function () {
      msg.style.transition = "opacity 0.5s ease";
      msg.style.opacity    = "0";
      setTimeout(function () { msg.remove(); }, 500);
    }, 4000); // Hide after 4 seconds
  });
}
