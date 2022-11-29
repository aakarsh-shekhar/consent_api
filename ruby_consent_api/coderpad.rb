require 'securerandom'
require 'date'

# consent = {
#   id
#   name
#   consent_url
#   created_at
#   versioconsent_urln
# }

# all_consents = {
#   id1: [consent1, consent1_version2, ...],
#   id2: [consent2],
#   ...
# }

$all_consents = {}

def get_consent(targetId)
  return $all_consents[targetId]
end

def get_consents
  return $all_consents
end

def create_consent(name, consent_url)
  new_consent_id = SecureRandom.uuid

  new_consent = {
    id: new_consent_id,
    name: name,
    consent_url: consent_url,
    created_at: DateTime.now,
    version: 0
  }

  $all_consents[new_consent_id] = [new_consent]

  $all_consents[new_consent_id]
end

def update_consent(targetId, consent_url)
  all_consent_versions = $all_consents[targetId]
  latest_version = all_consent_versions.last()

  new_consent = {
    id: latest_version[:id],
    name: latest_version[:name],
    consent_url: consent_url,
    created_at: DateTime.now,
    version: latest_version[:version] + 1
  }

  new_list = all_consent_versions.append(new_consent)
  $all_consents[latest_version[:id]] = new_list
end

create_consent("name1", "consent_url1")
# create_consent("name2", "consent_url2")

puts get_consents

test_id = get_consents.keys[0]

update_consent(test_id, "consent_url1_v2")
puts get_consents
