Rails.application.routes.draw do
  resources :oauth_clients
  get '/oauth/test_request',  :to => 'oauth#test_request',  :as => :test_request
  get '/oauth/token',         :to => 'oauth#token',         :as => :token
  get '/oauth/access_token',  :to => 'oauth#access_token',  :as => :access_token
  get '/oauth/request_token', :to => 'oauth#request_token', :as => :request_token
  get '/oauth/authorize',     :to => 'oauth#authorize',     :as => :authorize
  get '/oauth',               :to => 'oauth#index',         :as => :oauth
  devise_for :users
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  root :to => "oauth_clients#index"

end
