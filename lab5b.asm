; Lab 5b
; Single-step through the code in your mind. Keep track of each MEMORY read/write made by the processor (ignore I/O)

; Constant definitions
Display	EQU 04E9h	; address of Virgo display

ORG 0010h
; Data segment
STR: DB 'Hi$'
COUNT: DW	00

ORG 0020h
; Code segment

;;;;;;;;;;;;;;;;;
; countStr: Subroutine to count length of a '$'-terminated string
; Input parameters:
; 	SI: Address of start of string to be printed
; Output parameters:
;	BX: Count of characters in string, not including '$'.
countStr:
	; Save registers modified by this subroutine
	PUSH AX

	MOV BX, 0			; Reset counter
LoopCS:
	MOV AL, [SI+BX]		; Load the next char 
	CMP AL, '$'			; Compare the char to '$'
	JE quitCS			; If it is equal, then quit subroutine and return to calling code
	INC BX				; Point to the next char to be counted
	jmp LoopCS			; Jump back to the top of the loop
quitCS:
	; Restore registers
	POP AX
	RET

main:
	MOV SP, 0000h		; Initialize the SP
	MOV SI, STR			; Load the starting address of the string to be printed
	CALL countStr		; Call printStr to print the string
	MOV [COUNT],BX		; Save length of STR to variable COUNT
	HLT					; Quit
	
end main
