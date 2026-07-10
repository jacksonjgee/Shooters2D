@tool
extends StaticBody2D

@onready var color_rect: ColorRect = $ColorRect
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	update_collision_shape()

func update_collision_shape() -> void:
	if not is_instance_valid(color_rect):
		color_rect = get_node("ColorRect")

	if not is_instance_valid(collision_shape):
		collision_shape = get_node("CollisionShape2D")

	var rectangle := collision_shape.shape as RectangleShape2D

	if rectangle == null:
		rectangle = RectangleShape2D.new()
		collision_shape.shape = rectangle

	rectangle.size = color_rect.size

	# ColorRect position refers to its top-left corner.
	# CollisionShape2D position refers to its centre.
	collision_shape.position = color_rect.position + color_rect.size / 2.0
