extends CharacterBody2D

enum Teams {
	ATTACKER,
	DEFENDER
}

@onready var sprite: Sprite2D = $Sprite2D
@onready var bullet_tracer: Line2D = $BulletTracer

var speed = 300
var health = 100
@export var team: Teams = Teams.ATTACKER

@export var attacker_texture: Texture2D = preload("res://assets/player/attacker.png")
@export var defender_texture: Texture2D = preload("res://assets/player/defender.png")


func _ready():
	update_team_sprite()

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("left_click"):
		var direction: Vector2 = global_position.direction_to(
			get_global_mouse_position()
		)

		shoot(direction)

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
	
func update_team_sprite():
	match team:
		Teams.ATTACKER:
			sprite.texture = attacker_texture

		Teams.DEFENDER:
			sprite.texture = defender_texture

func shoot(direction: Vector2) -> void:
	var start_position: Vector2 = global_position
	var ray_length: float = 1000.0
	var end_position: Vector2 = start_position + direction * ray_length

	var query = PhysicsRayQueryParameters2D.create(
		start_position,
		end_position
	)

	query.exclude = [self]

	var result = get_world_2d().direct_space_state.intersect_ray(query)

	if result:
		end_position = result.position

	show_tracer(start_position, end_position)

func show_tracer(start_position: Vector2, end_position: Vector2) -> void:
	bullet_tracer.clear_points()

	bullet_tracer.add_point(to_local(start_position))
	bullet_tracer.add_point(to_local(end_position))

	await get_tree().create_timer(0.05).timeout

	bullet_tracer.clear_points()

func take_damage(amount: int) -> void:
	health =- amount
	print(health)
	
	if health <= 0:
		die()

func die() -> void:
	queue_free()
	
