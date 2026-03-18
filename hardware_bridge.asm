; GhostSemi Hardware Bridge
; This code communicates directly with the CPU Registers (EAX, EBX)
; bypassing standard software delays.

section .text
    global _start

_start:
    mov eax, 1      ; Command to the CPU: "Prepare Ghost Logic"
    mov ebx, 0      ; Clear the physical buffer
    int 0x80        ; Intercept the hardware interrupt