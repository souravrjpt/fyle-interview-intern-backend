

from flask import Blueprint
from core.apis import decorators
from core.apis.assignments.schema import AssignmentGradeSchema, AssignmentSchema, TeacherSchema
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core import db
from core.models.teachers import Teacher

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_graded_assignments(p):
    """List all submitted and graded assignments"""
    submitted_graded_assignments = Assignment.get_submitted_graded_assignments()

    submitted_graded_assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=submitted_graded_assignments_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all the teachers"""
    list_teachers = Teacher.list_teachers()

    list_teachers_dump = TeacherSchema().dump(list_teachers, many=True)
    return APIResponse.respond(data=list_teachers_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_regrade_assignments(p, incoming_payload):
    """Grade or re-grade an assignment"""
    assignment_grade_schema = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.mark_principal_grade(
        assignment_grade_schema.id
        ,assignment_grade_schema.grade
        ,auth_principal=p)
    
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    
    return APIResponse.respond(data=graded_assignment_dump)