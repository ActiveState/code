require 'net/https'


# Allows to make GET or POST requests to the facebook API graph
# the url parameter is the last part of the fb url excluding the https:/graph.facebook.com/
# It returns a dict from a JSON data structure.
#
# Note: You can also use open-uri for simple GET requests like this:
# obj = JSON.parse(open("https://graph.facebook.com/#{uid}?fields=id&access_token=#{access_token}").read)
# The problem is that in case
# of errors it raises a 400 HTTPBadRequest and it doesn't return any content of the body.
# Therefore, since the errors of a facebook request are inside the body of the response
# you couldn't get any fb errors from the simple function open.
def fb_api(url, access_token, attach = {}, request_type="GET")
  uri = URI("https://graph.facebook.com/#{url}")

  if request_type == "GET"
    uri.query = URI.encode_www_form(attach.merge('access_token' => access_token))
    req = Net::HTTP::Get.new uri.request_uri

  elsif request_type == "POST"
    req = Net::HTTP::Post.new(uri.path)
    req.set_form_data(attach.merge('access_token' => access_token))
  end


  res = Net::HTTP.new(uri.host, uri.port)
  res.verify_mode = OpenSSL::SSL::VERIFY_NONE
  res.use_ssl = true

  response = nil
  res.start do |http|
    response = http.request(req)
  end

  return JSON.parse(response.read_body)
end

def put_post_wall(profile_id, access_token, message, attach = {})
  fb_api("#{profile_id}/feed", access_token, attach.merge({'message'=>message}), request_type="POST")
end
