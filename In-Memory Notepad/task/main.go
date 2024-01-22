package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Note struct {
	description string
}

type Notes struct {
	notes []Note
}

func (notes *Notes) AddNote(note *string, limit *int) {
	if len(strings.TrimSpace(*note)) < 1 {
		fmt.Println("[Error] Missing note argument")
	} else if !notes.LimitNotExceed(limit) {
		fmt.Println("[Error] Notepad is full")
		return
	} else {
		notes.notes = append(notes.notes, Note{description: *note})
		fmt.Println("[OK] The note was successfully created")
	}
}

func (notes *Notes) LimitNotExceed(limit *int) bool {
	return len(notes.notes) < *limit
}

func (notes *Notes) Clear() {
	notes.notes = nil
	fmt.Println("[OK] All notes were successfully deleted")
}

func (notes *Notes) HasIndex(index *int) bool {
	return *index-1 >= 0 && *index-1 <= len(notes.notes) && len(notes.notes) > 0
}

func (notes *Notes) Delete(data *string) {
	if len(strings.TrimSpace(*data)) < 1 {
		fmt.Println("[Error] Missing position argument")
		return
	}
	index, err := strconv.Atoi(*data)
	if err != nil {
		fmt.Printf("[Error] Invalid position: %s\n", *data)
	} else {
		if notes.HasIndex(&index) {
			notes.notes = append(notes.notes[:index-1], notes.notes[index:]...)
			fmt.Printf("[OK] The note at position %d was successfully deleted\n", index)
		} else {
			fmt.Println("[Error] There is nothing to delete")
		}
	}
}

func (notes *Notes) Update(data *string, limit *int) {
	if len(strings.TrimSpace(*data)) < 1 {
		fmt.Println("[Error] Missing position argument")
		return
	}
	input := strings.Split(*data, " ")
	indexString, text := input[0], strings.Join(input[1:], " ")
	if len(strings.TrimSpace(text)) < 1 {
		fmt.Println("[Error] Missing note argument")
		return
	}
	index, err := strconv.Atoi(indexString)
	if err != nil {
		fmt.Printf("[Error] Invalid position: %s\n", indexString)
	} else if *limit < index {
		fmt.Printf("[Error] Position %d is out of the boundaries [1, %d]\n", index, *limit)
	} else {
		if notes.HasIndex(&index) {
			notes.notes[index-1].description = text
			fmt.Printf("[OK] The note at position %d was successfully updated\n", index)
		} else {
			fmt.Println("[Error] There is nothing to update")
		}
	}
}

func (notes *Notes) ListNotes() {
	switch len(notes.notes) {
	case 0:
		fmt.Println("[Info] Notepad is empty")
	default:
		for index, note := range notes.notes {
			fmt.Printf("[Info] %d: %s\n", index+1, note.description)
		}
	}
}

func ProcessCommand(state *bool, notes *Notes, limit *int) {
	fmt.Print("Enter a command and data: ")

	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()

	input := strings.Split(scanner.Text(), " ")
	command, data := input[0], strings.Join(input[1:], " ")

	switch command {
	case "exit":
		fmt.Printf("[INFO] Bye!")
		*state = false
	case "list":
		notes.ListNotes()
	case "create":
		notes.AddNote(&data, limit)
	case "clear":
		notes.Clear()
	case "delete":
		notes.Delete(&data)
	case "update":
		notes.Update(&data, limit)
	default:
		fmt.Println("[Error] Unknown command")
	}
	fmt.Printf("\n")
}

func main() {
	var notes Notes
	state := true
	var limit int
	fmt.Printf("Enter the maximum number of notes: ")
	_, err := fmt.Scan(&limit)
	if err != nil {
		return
	}
	for state {
		ProcessCommand(&state, &notes, &limit)
	}
}
