
from flask import Blueprint, request, render_template, jsonify, abort
from flask_sqlalchemy_session import current_session as session

from featuresreq.models import Client, FeatureRequest
from featuresreq.schemas import ClientSchema, FeatureRequestSchema

bp = Blueprint('public', __name__, template_folder='templates', static_folder='static')


@bp.route('/')
def public_html():
    return render_template("feature_form.jinja")


@bp.route('/api/clients')
def clients():
    clients = session.query(Client).order_by(Client.name).all()
    schema = ClientSchema(session=session)
    data, errors = schema.dump(clients, many=True)
    return jsonify(data), 200


@bp.route('/api/features', methods=["POST"])
def features():
    """
    Create a new feature
    """
    schema = FeatureRequestSchema(session=session)
    jdata = request.get_json(force=True)
    data, errors = schema.load(jdata)

    if errors:
        return jsonify({
            "errors": errors,
            "success": False,
        }), 400

    client = session.query(Client).filter(Client.id == data.client_id).first()
    if not client:
        return jsonify({
            "errors": {"client_id": ["No client with this id exists."]},
            "success": False,
        }), 400

    add_feature_request(feature=data)
    for f in session.query(FeatureRequest).all():
        print(f.id, f.client_id, f.priority)

    return jsonify({
        "success": True,
    }), 200


def add_feature_request(feature):
    """
    Adds a feature to the database, handles updating conflicting priorities.

    Note: This should be reimplemented to use a priority queue
    """
    client_id = feature.client_id
    new_feature = session.query(FeatureRequest.id, FeatureRequest.priority).filter(
            FeatureRequest.client_id == client_id,
            FeatureRequest.priority == feature.priority).first()

    if new_feature is not None:
        feature_id, priority = new_feature
        increment_priority(
            feature_id=feature_id,
            client_id=client_id,
            priority=priority)

    session.add(feature)
    session.commit()


def increment_priority(feature_id, client_id, priority):
    """Recursively increments the feature request priority."""
    new_priority = priority + 1
    new_feature_id = session.query(FeatureRequest.id).filter(
            FeatureRequest.client_id == client_id,
            FeatureRequest.priority == new_priority).first()

    if new_feature_id:
        increment_priority(
            feature_id=new_feature_id[0],
            client_id=client_id,
            priority=new_priority)

    session.query(FeatureRequest).filter(
        FeatureRequest.id == feature_id
    ).update({"priority": new_priority})
    session.commit()
