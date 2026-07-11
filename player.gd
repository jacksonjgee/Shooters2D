extends CharacterBody2D

enum Teams {
	ATTACKER,
	DEFENDER
}

@onready var sprite: Sprite2D = $Sprite2D

var speed = 300
var health = 100
@export var team: Teams = Teams.ATTACKER

@export var attacker_texture: Texture2D = preload("res://assets/player/attacker.png")
@export var defender_texture: Texture2D = preload("res://assets/player/defender.png")


func _ready():
	update_team_sprite()


func update_team_sprite():
	match team:
		Teams.ATTACKER:
			sprite.texture = attacker_texture

		Teams.DEFENDER:
			sprite.texture = defender_texture


func _physics_process(_delta):
	var direction = Vector2.ZERO

	if Input.is_action_pressed("move_right"):
		direction.x += 1

	if Input.is_action_pressed("move_left"):
		direction.x -= 1

	if Input.is_action_pressed("move_down"):
		direction.y += 1

	if Input.is_action_pressed("move_up"):
		direction.y -= 1

	if direction.length() > 0:
		direction = direction.normalized()

	velocity = direction * speed
	move_and_slide()

	look_at(get_global_mouse_position())
