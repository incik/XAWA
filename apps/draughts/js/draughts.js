/** 
 * Created by Tomáš Vaisar, 2011
 * tomas.vaisar@gmail.com, xvaisa00@stud.fit.vutbr.cz
 *
 * Released under GNU/LGPL
 */

// CONFIGURATION FOR XAWA PLUGIN
var XAWA_APP_CONFIG = {
	appName : "Draughts - Simple board game",
	appUrl : "http://xawa.vaisar.cz/apps/draughts/",
	__window : {
		width : 900,
		height : 760 
	}
}

// GLOBAL SETTINGS
// it reflects current state of game
var GLOBALS = {
	currentPlayer : 1,
	playerCanContinue : false,
	__player1 : "white",
	__player2 : "black",
	__player1Score : 0,
	__player2Score : 0,
	__userIsPlayer : 1, // set by xawa negotiation
}

function switchPlayers() {
	if (GLOBALS.currentPlayer == 1) GLOBALS.currentPlayer = 2;
	else GLOBALS.currentPlayer = 1;

	GLOBALS.playerCanContinue = false;
}

function playerCanPlayAgain() {
	GLOBALS.playerCanContinue = true;
	if (GLOBALS.currentPlayer == GLOBALS.__userIsPlayer) {
		$('#skipTurnButton').removeAttr('disabled');
	}
}

function skipThisTurn() {
	$('#skipTurnButton').attr('disabled','disabled');
	switchPlayers();
}

// @param element - piece of DOM as jQ object
function getCoords(element) {
	var true_y = (function () {
		var rows = $('.row');
		var elementrow = element.parent().parent()[0];
		for (var i in rows) {
			if (rows[i] == elementrow)
				return i;
		}
		return -1;
	})();
	var human_y = element.parent().parent().children().first().html();
	var human_x = (function () {
		var childs = element.parent().parent().children();
		for (i in childs) {
			if ($(childs[i]).children().index(element) != -1)
				return i;
		}
		return -1;
	})();
	var true_x = human_x; // ... yeah, they're the same :)
	return { "x": true_x, "y": true_y, "human_x": human_x, "human_y" : human_y };
}

// @param coords - 
function isFieldEmpty(coords) {
	return getField(coords).find('div.piece').length == 1 ? false : true;
}

function isDropFieldEmpty(coords) {
	return getField(coords).find('div.piece').length > 1 ? false : true;
}

function isTheWayEmpty(startCoords, finishCoords) {
	// this test should be for long jumps only
	if ((startCoords.x - finishCoords.x) == 2 || (startCoords.y - finishCoords.y) == 2 
		|| (finishCoords.x - startCoords.x) == 2 || (finishCoords.y - startCoords.y) == 2)
		return true;
		
	// all the way must be clean (we can't jump over six pieces and take the last one)
	if (startCoords.x > finishCoords.x) { // left
		if (startCoords.y > finishCoords.y) { // up
			for (var i = startCoords.x - 1, j = startCoords.y - 1; i > (parseInt(finishCoords.x) + 1); i--, j--) {
				if (!isFieldEmpty({ "x": i, "y": j }))
					return false;
			}
		} else if (startCoords.y < finishCoords.y) { // down
			for (var i = startCoords.x - 1, j = parseInt(startCoords.y) + 1; i > (parseInt(finishCoords.x) + 1); i--, j++) {
				if (!isFieldEmpty({ "x": i, "y": j }))
					return false;
			}
		}
	} else if (startCoords.x < finishCoords.x) { // right
		if (startCoords.y > finishCoords.y) { // up
			for (var i = parseInt(startCoords.x) + 1, j = startCoords.y - 1; i < (finishCoords.x - 1); i++, j--) {
				if (!isFieldEmpty({ "x": i, "y": j }))
					return false;
			}
		} else if (startCoords.y < finishCoords.y) { // down
			for (var i = parseInt(startCoords.x) + 1, j = parseInt(startCoords.y) + 1; i < (finishCoords.x - 1); i++, j++) {
				if (!isFieldEmpty({ "x": i, "y": j }))
					return false;
			}
		}
	}
	
	return true;
}

function isThatPieceMine(piece) {
	return ((piece.hasClass(GLOBALS.__player1) && GLOBALS.currentPlayer == 1)
		|| (piece.hasClass(GLOBALS.__player2) && GLOBALS.currentPlayer == 2)) ? true : false;
}

function isItMaster(piece) {
	return piece.hasClass('master');
}

function getField(coords) {
	return $($($('table#board tr.row')[coords.y]).children()[coords.x]);
}

function getPiece(coords) {
	return getField(coords).find('div.piece');
}

function removePiece(piece) {
	piece.effect('highlight', {}, 250, function() {
		piece.remove();
	});
}

// @param move - array with original coordinates and final coordinates (i.e. [[5,3],[6,4]] )
// @param piece - the element witch is currently moved
// @param options - nonrequired param with additional options modifying behavior
function validateMove(move, piece, options) {
	var start = move[0];
	var finish = move[1];
	
	// is that field even empty?
	if (!isDropFieldEmpty(finish))
		return false;
	
	// you can't move horizontally or vertically
	if ((start.x == finish.x) || (start.y == finish.y))
		return false;
	
	if (isItMaster(piece)) {
		// it can - jump much longer distances
		//        - go backwards
		
		if ((start.x - finish.x) > 1 || (start.y - finish.y) > 1 
			|| (finish.x - start.x) > 1 || (finish.y - start.y) > 1)
		{
			var x_move = start.x - finish.x;
			var y_move = start.y - finish.y;

			var coords = {};
			if (x_move > 0) { // left
				if (y_move < 0) { // down
					coords = {"x": parseInt(finish.x) + 1, "y": parseInt(finish.y) - 1};
				} else { // up
					coords = {"x": parseInt(finish.x) + 1, "y": parseInt(finish.y) + 1};
				}
			}
			else if (x_move < 0) // right
			{
				if (y_move < 0) { // down
					coords = {"x": parseInt(finish.x) - 1, "y": parseInt(finish.y) - 1};
				} else { // up
					coords = {"x": parseInt(finish.x) - 1, "y": parseInt(finish.y) + 1};
				}
			}
			
			if (options !== undefined && options.skipMineFieldDetection == true) {
				// nop
			} else if (isThatPieceMine(getPiece(coords))) {
				return false;
			}
			
			if (isTheWayEmpty(start, finish) && !isFieldEmpty(coords) && !isThatPieceMine(getPiece(coords))) {
				updateScore(GLOBALS.currentPlayer);
				removePiece(getPiece(coords)); // nom non nom nom
				playerCanPlayAgain();
			}
			else if (isTheWayEmpty(start, finish) && !isThatPieceMine(getPiece(coords))) { // this is just regular move
				return true;
			}
			else
				return false;
		}
	}
	// "nom nom" jump
	else if ((start.x - finish.x) == 2 || (start.y - finish.y) == 2 
		|| (finish.x - start.x) == 2 || (finish.y - start.y) == 2)
	{
		var x_move = start.x - finish.x;
		var y_move = start.y - finish.y;

		var coords = {};
		if (x_move > 0) { // left
			if (y_move < 0) { // down
				coords = {"x": start.x - 1, "y": parseInt(start.y) + 1};
			} else { // up
				coords = {"x": start.x - 1, "y": start.y - 1};
			}
		}
		else if (x_move < 0) // right
		{
			if (y_move < 0) { // down
				coords = {"x": parseInt(start.x) + 1, "y": parseInt(start.y) + 1};
			} else { // up
				coords = {"x": parseInt(start.x) + 1, "y": start.y - 1};
			}
		}
		
		if (options !== undefined && options.skipMineFieldDetection == true) {
			// nop
		} else if (isThatPieceMine(getPiece(coords))) {
			return false;
		}
			
		if (!isFieldEmpty(coords)) { // && !isThatPieceMine(getPiece(coords))) { 
			updateScore(GLOBALS.currentPlayer);
			removePiece(getPiece(coords)); // nom non nom nom
			playerCanPlayAgain();
		}
		else
			return false;
	}	
	
	// white pieces can only go up and black can go only down
	else if ((piece.hasClass(GLOBALS.__player1) && ((finish.y - start.y) > 0))
		|| (piece.hasClass(GLOBALS.__player2) && ((start.y - finish.y) > 0)))
		return false;
	
	// otherwise basic jump must be 1 field long 
	else if ((start.x - finish.x) > 1 || (start.y - finish.y) > 1 
		|| (finish.x - start.x) > 1 || (finish.y - start.y) > 1)
		return false;
		
	// if the piece reaches opponent's side, it transforms into the masterpiece!
	if ((piece.hasClass(GLOBALS.__player1) && finish.y == 0)
		|| (piece.hasClass(GLOBALS.__player2) && finish.y == 7))
		if (!isItMaster(piece)) piece.addClass('master');
			
	return true;
}

// @param to - field where we're going to
// @param piece - the element witch is currently moved
// @return - new coordinates of piece
function move(to, piece) {
	to.append(piece);
	piece.css("left","0").css("top","0");
	return getCoords(piece);
}

//
// @param move - array with original coordinates and final coordinates (i.e. [[5,3],[6,4]] )
function logMove(move) {
	var log = new Array();
	var letters = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
	log.push('<li>['); log.push(letters[move[0].human_x]); log.push(','); log.push(move[0].human_y);
	log.push('] &rarr; [');
	log.push(letters[move[1].human_x]); log.push(',');	log.push(move[1].human_y); log.push(']</li>');	
	$('#movementHistory ul').html($('#movementHistory ul').html() + log.join(''));	
}

function __initGame() {
	// rendering of playboard	
	$.each($('#board .row'), function(i,el_i) {
		$.each($(el_i).find('.field'), function(j,el_j) {		
			if ((j + i) % 2 == 1)
				$(el_j).addClass('blackfield');
		});		
	});
	
	// set player1 as starter
	GLOBALS.currentPlayer = 1;
	
	// show initial score
	showScore();
	
	// show menu
	showMenu();
}

function showMenu() {
	$('#menu').dialog({
		modal : true,
		draggable: false,
		resizable: false,
		closeOnEscape: false,
		open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); }
	});
}

function hideMenu() {
	$('#menu').dialog('close');	
}

function updateGameInfo() {
	$('#currentPlayer strong').html(GLOBALS.currentPlayer == 1 ? GLOBALS.__player1 : GLOBALS.__player2);
}

function updateScore(player) {
	if (player == 1)
		GLOBALS.__player1Score++;
	else if (player == 2)
		GLOBALS.__player2Score++;
	
	showScore();
}

function showScore() {
	if (GLOBALS.__userIsPlayer == 1) {
		$('#yourScore strong').html(GLOBALS.__player1Score);
		$('#opponentsScore strong').html(GLOBALS.__player2Score);
	}
	else if (GLOBALS.__userIsPlayer == 2) {
		$('#yourScore strong').html(GLOBALS.__player2Score);
		$('#opponentsScore strong').html(GLOBALS.__player1Score);
	}
}

function __registerEventHandlers() {
	// function handling incomming messages
	onApplicationReady = function() {
		xawa.sendData({ ready : true });
	};
	
	onDataReceived = function(data) {
		var recv = JSON.parse(data);
		// what did we received?
		if (recv.ready !== undefined) {
			xawa.sendData({ negotiate: true, player : 2 });
		} else if (recv.move !== undefined) { // move?
			var coords = recv.move;
			var start = coords[0];
			var finish = coords[1];
		
			var piece = getPiece(start);
			move(getField(finish), piece);
			if (validateMove(coords, piece, { skipMineFieldDetection : true })) {
				logMove(coords);
				updateGameInfo();
			}
		} else if (recv.switchPlayers !== undefined) {
			switchPlayers();
		} else if (recv.skipTurn !== undefined) {
			skipThisTurn();
		} else if (recv.negotiate !== undefined) {
			hideMenu();
			GLOBALS.__userIsPlayer = recv.player;
			xawa.sendData({ startGame: true });
		} else if (recv.startGame !== undefined) {
			hideMenu();
		}
	};
	
	onSessionLeave = function() {
		alert(xawa.recipient + ' has left the game. You win!');
		window.location = window.location; // the cleanest way to reload app ...
	};
}

$(document).ready(function() {
	
	__initGame();
	__registerEventHandlers();
	updateGameInfo();
	
	$('#inviteButton').click(function() {
		xawa.invite(xawa.recipient, XAWA_APP_CONFIG, {
			onAccept: function() { hideMenu(); },
			onRefuse: function() { alert(xawa.recipient + " doesn't want to play."); }
		});
	});
	
	$('#startButton').click(function() {
		xawa.sendData({ negotiate: true, player : 2 });
	});
	
	$('#closeButton').click(function() {
		if (confirm('Do you really want to abandon current game?')) {
			xawa.leave();
			window.history.back(); // not really clean solution but it works ... 
		}
	});
	
	$('div.piece').draggable({ revert: "invalid",
		drag: function() {
			var valid = true;
			// check if we can play
			if (GLOBALS.__userIsPlayer != GLOBALS.currentPlayer)
				valid = false;
		
			// hey! don't touch opponent's pieces!
			if ($(this).hasClass(GLOBALS.__player1) && GLOBALS.currentPlayer != 1)
				valid = false;
			else if ($(this).hasClass(GLOBALS.__player2) && GLOBALS.currentPlayer != 2)
				valid = false;
		
			if (!valid) {
				return false;
			}
		}	
	});
	
	$('#skipTurnButton').click(function() {
		skipThisTurn();
		xawa.sendData({ skipTurn: true });
		return false;
	})
	
	$('.blackfield').droppable(
		{
			drop: function(event, ui) { 
				
				var originalField = $(ui.draggable[0]).parent();
				var destinationField = $($(this)[0]);
											
				var piece = $(ui.draggable[0]);
				var originalPosition = getCoords(piece);
				var finalPosition = move(destinationField, piece);
				var moveCoords = [originalPosition, finalPosition];
				// check if it's valid move
				if (validateMove(moveCoords, piece)) {
					// send the move through XAWA
					xawa.sendData({ move : moveCoords });
					logMove(moveCoords);
					if (!GLOBALS.playerCanContinue) {
						switchPlayers();
						xawa.sendData({ switchPlayers: true });
					}
					updateGameInfo();
				} else { // that move wasn't valid
					move(originalField, piece);
				}
				
			} 
		}
	);
});
