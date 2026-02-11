import "./MyButton.css"

interface MyButtonProps {
    label: string
    onClick?: () => void
    className?: string
}

export default function MyButton({label, onClick, className}: MyButtonProps) {
    return (
        <button className={`my-button ${className ?? ''}`} onClick={onClick}>{label}</button>
    )
}